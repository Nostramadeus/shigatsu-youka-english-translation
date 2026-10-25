"""Carry accepted lettering onto a registered, shaded planar animation surface."""
import cv2
import numpy as np


def carry(original, english, frame, corners, visible=None):
    height, width = frame.shape[:2]
    page_height, page_width = original.shape[:2]
    if original.shape != english.shape:
        raise ValueError("Accepted English face dimensions differ")
    matrix = cv2.getPerspectiveTransform(np.float32([[0, 0], [page_width, 0],
                                                   [page_width, page_height], [0, page_height]]), np.float32(corners))
    coverage = cv2.warpPerspective(np.full(original.shape[:2], 255, np.uint8), matrix, (width, height))
    mask = cv2.erode(coverage, np.ones((7, 7), np.uint8))
    if visible is not None:
        mask[~visible] = 0
    warped = cv2.warpPerspective(original, matrix, (width, height))
    gray_original = cv2.cvtColor(warped[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
    gray_frame = cv2.cvtColor(frame[:, :, :3], cv2.COLOR_RGB2GRAY).astype(np.float32)
    try:
        correlation, correction = cv2.findTransformECC(gray_frame, gray_original, np.eye(3, dtype=np.float32),
            cv2.MOTION_HOMOGRAPHY, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 1e-5), mask, 5)
        matrix = np.linalg.inv(correction) @ matrix
    except cv2.error:
        correlation = None
    warped_original = cv2.warpPerspective(original, matrix, (width, height)).astype(float)
    warped_english = cv2.warpPerspective(english, matrix, (width, height)).astype(float)
    coverage = cv2.warpPerspective(np.full(original.shape[:2], 255, np.uint8), matrix, (width, height))
    inner = (cv2.erode(coverage, np.ones((7, 7), np.uint8)) == 255) & (frame[:, :, 3] == 255)
    if visible is not None:
        inner &= visible
    if inner.sum() < 100:
        raise ValueError("Insufficient visible surface for a shading fit")
    coefficients, residuals = [], []
    for channel in range(3):
        values = warped_original[:, :, channel][inner]
        target = frame[:, :, channel][inner]
        coefficients.append(np.linalg.lstsq(np.column_stack((values, np.ones(len(values)))), target, rcond=None)[0])
        gain, offset = coefficients[-1]
        residuals.append(float(np.abs(gain * values + offset - target).mean()))
    residual = float(np.mean(residuals))
    if residual > 12:
        raise ValueError("Surface registration residual %.2f exceeds the existing 12-level gate" % residual)
    changed = (np.max(np.abs(english[:, :, :3].astype(int) - original[:, :, :3].astype(int)), axis=2) > 5).astype(np.uint8)
    changed = cv2.dilate(changed, np.ones((3, 3), np.uint8))
    selected = (cv2.warpPerspective(changed, matrix, (width, height)) > 0) & (coverage > 250) & (frame[:, :, 3] == 255)
    if visible is not None:
        selected &= visible
    gains = np.array([coefficient[0] for coefficient in coefficients])
    offsets = np.array([coefficient[1] for coefficient in coefficients])
    shaded = warped_english[:, :, :3] * gains + offsets
    result = frame.copy()
    result[selected, :3] = np.clip(np.round(shaded[selected]), 0, 255).astype(np.uint8)
    return result, selected, coverage, dict(matrix=matrix.tolist(), correlation=correlation,
        coefficients=np.array(coefficients).tolist(), fitted_residual=residual, changed_pixels=int(selected.sum()))
