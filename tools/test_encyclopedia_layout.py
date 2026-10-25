import copy
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from livemaker.lsb import LMScript
from livemaker.lsb.core import OpeData, OpeDataType, OpeFuncType, Param, ParamType


ROOT = Path(__file__).resolve().parent.parent
FIX = ROOT / 'patch' / 'fix-00001878.py'
PLACE_IDX = 834


class PlaceScrollBufferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = ROOT / 'work' / '00001878.lsb'
        cls.original = source.read_bytes()
        cls.original_script = LMScript.from_lsb(cls.original)
        if str(cls.original_script.commands[PLACE_IDX]['PR_HEIGHT']) == '20000':
            cls.original_script.commands[PLACE_IDX]['PR_HEIGHT'].entries = [
                OpeData(type=OpeDataType.To, name='____0',
                        operands=[Param(value='テキスト矩形', type=ParamType.Str)]),
                OpeData(type=OpeDataType.Func, name='____1', func=OpeFuncType.GetProp,
                        operands=[Param(value='____0', type=ParamType.Var), Param(value=6, type=ParamType.Int)]),
                OpeData(type=OpeDataType.Minus, name='____2',
                        operands=[Param(value='____1', type=ParamType.Var), Param(value=5, type=ParamType.Int)]),
                OpeData(type=OpeDataType.To, name='____arg',
                        operands=[Param(value='____2', type=ParamType.Var)])]
            cls.original = cls.original_script.to_lsb()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / 'source.lsb'
        self.output = Path(self.temp.name) / 'output.lsb'
        self.source.write_bytes(self.original)

    def run_patch(self, source=None, output=None):
        return subprocess.run(
            [sys.executable, str(FIX), str(source or self.source), str(output or self.output)],
            capture_output=True, text=True, encoding='utf-8',
            env={**os.environ, 'PYTHONUTF8': '1'})

    def assert_refused(self):
        result = self.run_patch()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.output.exists())

    def test_changes_only_initial_place_height(self):
        original_place = self.original_script.commands[PLACE_IDX]
        self.assertEqual(original_place.type.name, 'MesNew')
        self.assertEqual(str(original_place['Name']), '"場所詳細"')
        self.assertEqual(str(original_place['PR_HEIGHT']), 'GetProp("テキスト矩形", 6) - 5')
        result = self.run_patch()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        patched = LMScript.from_lsb(self.output.read_bytes())
        self.assertEqual(str(patched.commands[PLACE_IDX]['PR_HEIGHT']), '20000')
        for sibling in (1406, 1670):
            self.assertEqual(str(patched.commands[sibling]['PR_HEIGHT']), '20000')
        patched.commands[PLACE_IDX]['PR_HEIGHT'].entries = copy.deepcopy(original_place['PR_HEIGHT'].entries)
        self.assertEqual(patched.to_lsb(), self.original)

    def test_already_applied_is_byte_identical(self):
        first = self.run_patch()
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        expected = self.output.read_bytes()
        second = self.run_patch(self.output, self.output)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        self.assertEqual(self.output.read_bytes(), expected)

    def test_rejects_changed_name_before_writing(self):
        script = LMScript.from_lsb(self.source.read_bytes())
        script.commands[PLACE_IDX]['Name'].entries[0].operands[0].value = 'Unexpected detail'
        self.source.write_bytes(script.to_lsb())
        self.assert_refused()

    def test_rejects_changed_height_before_writing(self):
        script = LMScript.from_lsb(self.source.read_bytes())
        script.commands[PLACE_IDX]['PR_HEIGHT'].entries = copy.deepcopy(script.commands[1406]['PR_HEIGHT'].entries)
        script.commands[PLACE_IDX]['PR_HEIGHT'].entries[0].operands[0].value = 20001
        self.source.write_bytes(script.to_lsb())
        self.assert_refused()

    def test_rejects_changed_command_before_writing(self):
        script = LMScript.from_lsb(self.source.read_bytes())
        script.commands[PLACE_IDX] = copy.deepcopy(script.commands[820])
        self.source.write_bytes(script.to_lsb())
        self.assert_refused()


if __name__ == '__main__':
    unittest.main()
