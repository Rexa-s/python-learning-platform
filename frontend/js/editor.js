/**
 * Code Editor Integration with CodeMirror
 */

class CodeEditor {
    constructor(elementId, options = {}) {
        this.elementId = elementId;
        this.element = document.getElementById(elementId);

        if (!this.element) {
            console.error(`Element with id '${elementId}' not found`);
            return;
        }

        // Initialize CodeMirror
        this.editor = CodeMirror(this.element, {
            mode: 'python',
            theme: 'default',
            lineNumbers: true,
            indentUnit: 4,
            indentWithTabs: false,
            lineWrapping: true,
            height: options.height || '400px',
            ...options
        });

        // Default content
        if (options.initialContent) {
            this.editor.setValue(options.initialContent);
        }
    }

    /**
     * Get the code from the editor
     */
    getCode() {
        return this.editor.getValue();
    }

    /**
     * Set the code in the editor
     */
    setCode(code) {
        this.editor.setValue(code);
    }

    /**
     * Clear the editor
     */
    clear() {
        this.editor.setValue('');
    }

    /**
     * Set read-only mode
     */
    setReadOnly(readOnly = true) {
        this.editor.setOption('readOnly', readOnly);
    }

    /**
     * Focus the editor
     */
    focus() {
        this.editor.focus();
    }

    /**
     * Get the line count
     */
    getLineCount() {
        return this.editor.lineCount();
    }

    /**
     * Run code and display output
     */
    async run(api, lessonId = null, exerciseId = null) {
        const code = this.getCode();

        if (!code.trim()) {
            alert('Lütfen kod yazınız!');
            return;
        }

        try {
            // Show loading state
            this.setReadOnly(true);

            const result = await api.executeCode(code, lessonId, exerciseId);

            if (result.success) {
                const execution = result.execution;
                if (execution.success) {
                    this.displayOutput(execution.output, 'success');
                } else {
                    this.displayOutput(execution.error, 'error');
                }
                return execution;
            } else {
                this.displayOutput(result.error, 'error');
            }
        } catch (error) {
            this.displayOutput(`Hata: ${error.message}`, 'error');
        } finally {
            this.setReadOnly(false);
        }
    }

    /**
     * Test code against test cases
     */
    async test(api, exerciseId, testCases, lessonId = null) {
        const code = this.getCode();

        if (!code.trim()) {
            alert('Lütfen kod yazınız!');
            return;
        }

        try {
            this.setReadOnly(true);

            const result = await api.testExercise(exerciseId, code, testCases, lessonId);

            if (result.success) {
                const testResult = result.test_result;

                let output = `Test Sonuçları: ${testResult.passed}/${testResult.total} başarılı\n`;
                output += '─'.repeat(40) + '\n\n';

                testResult.results.forEach((testCase, index) => {
                    output += `Test ${index + 1}: ${testCase.passed ? '✅ BAŞARILI' : '❌ BAŞARISIZ'}\n`;
                    if (!testCase.passed) {
                        output += `Beklenen: ${testCase.expected}\n`;
                        output += `Alınan: ${testCase.actual}\n`;
                        if (testCase.error) {
                            output += `Hata: ${testCase.error}\n`;
                        }
                    }
                    output += '\n';
                });

                this.displayOutput(output, testResult.success ? 'success' : 'warning');
                return testResult;
            } else {
                this.displayOutput(result.error, 'error');
            }
        } catch (error) {
            this.displayOutput(`Hata: ${error.message}`, 'error');
        } finally {
            this.setReadOnly(false);
        }
    }

    /**
     * Display output in console area
     */
    displayOutput(output, type = 'info') {
        const consoleEl = document.getElementById('console-output');
        if (consoleEl) {
            consoleEl.textContent = output;
            consoleEl.className = `console-output console-${type}`;
            consoleEl.style.display = 'block';
            consoleEl.scrollTop = consoleEl.scrollHeight;
        }
    }

    /**
     * Clear console output
     */
    clearOutput() {
        const consoleEl = document.getElementById('console-output');
        if (consoleEl) {
            consoleEl.textContent = '';
            consoleEl.style.display = 'none';
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CodeEditor;
}
