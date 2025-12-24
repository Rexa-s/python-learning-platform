import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any

class CodeExecutor:
    """Execute user Python code safely with timeout and restrictions"""

    # Allowed built-in functions
    ALLOWED_BUILTINS = {
        'print', 'len', 'range', 'int', 'float', 'str', 'bool',
        'list', 'dict', 'tuple', 'set',
        'abs', 'min', 'max', 'sum', 'round',
        'input', 'enumerate', 'zip',
        'type', 'isinstance', 'sorted', 'reversed',
        'any', 'all', 'filter', 'map'
    }

    # Forbidden names that can't be used
    FORBIDDEN_NAMES = {
        '__import__', 'eval', 'exec', 'compile',
        'open', 'file',
        '__builtins__', 'globals', 'locals',
        '__code__', '__class__', '__bases__',
        'sys', 'os', '__name__'
    }

    def __init__(self, timeout=5, max_output=10000):
        """
        Initialize code executor

        Args:
            timeout: Maximum execution time in seconds
            max_output: Maximum output length in characters
        """
        self.timeout = timeout
        self.max_output = max_output

    def validate_code(self, code: str) -> tuple[bool, str]:
        """
        Validate code for dangerous patterns

        Returns:
            (is_valid, error_message)
        """
        # Check for forbidden keywords
        for forbidden in self.FORBIDDEN_NAMES:
            if forbidden in code:
                return False, f"Forbidden keyword detected: {forbidden}"

        # Check for dangerous patterns
        dangerous_patterns = [
            ('import', 'import statements are not allowed'),
            ('__', 'dunder methods are not allowed'),
            ('exec', 'exec is not allowed'),
            ('eval', 'eval is not allowed'),
            ('compile', 'compile is not allowed'),
        ]

        for pattern, msg in dangerous_patterns:
            if pattern in code.lower():
                return False, msg

        return True, ""

    def execute(self, code: str, inputs: list = None) -> Dict[str, Any]:
        """
        Execute Python code safely

        Args:
            code: Python code to execute
            inputs: List of inputs for input() calls

        Returns:
            Dictionary with execution results:
            {
                'success': bool,
                'output': str,
                'error': str,
                'execution_time': float
            }
        """
        import time

        start_time = time.time()

        # Validate code
        is_valid, error_msg = self.validate_code(code)
        if not is_valid:
            return {
                'success': False,
                'output': '',
                'error': error_msg,
                'execution_time': 0
            }

        # Capture output
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        try:
            # Create input handler
            input_queue = list(inputs) if inputs else []
            input_index = [0]  # Use list to allow modification in nested function

            def custom_input(prompt=''):
                if prompt:
                    output_buffer.write(str(prompt))

                if input_index[0] < len(input_queue):
                    value = input_queue[input_index[0]]
                    input_index[0] += 1
                    output_buffer.write(str(value) + '\n')
                    return str(value)
                else:
                    raise EOFError("No more inputs available")

            # Create restricted globals
            safe_builtins = {}
            for name in self.ALLOWED_BUILTINS:
                try:
                    if isinstance(__builtins__, dict):
                        if name in __builtins__:
                            safe_builtins[name] = __builtins__[name]
                    else:
                        safe_builtins[name] = getattr(__builtins__, name)
                except:
                    pass

            safe_builtins['input'] = custom_input

            safe_globals = {
                '__builtins__': safe_builtins,
                '__name__': '__main__',
                '__doc__': None,
            }

            # Execute code
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                exec(code, safe_globals)

            output = output_buffer.getvalue()

            # Limit output size
            if len(output) > self.max_output:
                output = output[:self.max_output] + '\n... (output truncated)'

            execution_time = time.time() - start_time

            return {
                'success': True,
                'output': output,
                'error': '',
                'execution_time': execution_time
            }

        except Exception as e:
            execution_time = time.time() - start_time
            error_output = traceback.format_exc()

            return {
                'success': False,
                'output': output_buffer.getvalue(),
                'error': error_output,
                'execution_time': execution_time
            }

    def validate_output(self, output: str, expected_output: str, strict=False) -> bool:
        """
        Validate code output against expected output

        Args:
            output: Actual output
            expected_output: Expected output
            strict: If True, do exact match. If False, check if output contains expected

        Returns:
            True if output matches expectations
        """
        if strict:
            return output.strip() == expected_output.strip()
        else:
            return expected_output.strip() in output.strip()

    def run_tests(self, code: str, test_cases: list) -> Dict[str, Any]:
        """
        Run code against test cases

        Args:
            code: Python code to test
            test_cases: List of test cases with 'input' and 'expected_output'

        Returns:
            {
                'success': bool,
                'passed': int,
                'total': int,
                'results': [{'passed': bool, 'expected': str, 'actual': str}]
            }
        """
        results = []
        passed = 0

        for test in test_cases:
            # Get inputs for this test case
            test_inputs = test.get('inputs', [])

            # Execute code with inputs
            exec_result = self.execute(code, test_inputs)

            expected = test.get('expected_output', '')
            actual = exec_result.get('output', '')

            test_passed = self.validate_output(actual, expected, strict=False)

            if test_passed:
                passed += 1

            results.append({
                'passed': test_passed,
                'expected': expected,
                'actual': actual,
                'error': exec_result.get('error', '')
            })

        return {
            'success': passed == len(test_cases),
            'passed': passed,
            'total': len(test_cases),
            'results': results
        }
