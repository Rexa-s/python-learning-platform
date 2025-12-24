/**
 * Lesson Renderer
 * Converts lesson JSON to HTML and renders it
 */

class LessonRenderer {
    constructor() {
        this.currentLesson = null;
    }

    /**
     * Render a lesson into the provided container
     */
    async renderLesson(lesson, containerId) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`Container with id '${containerId}' not found`);
            return;
        }

        this.currentLesson = lesson;

        // Build HTML
        let html = `
            <div class="lesson-header">
                <h1>${this.escapeHtml(lesson.title)}</h1>
                <p class="lesson-description">${this.escapeHtml(lesson.description || '')}</p>
            </div>
        `;

        // Render sections
        if (lesson.sections && lesson.sections.length > 0) {
            html += '<div class="lesson-content">';

            for (const section of lesson.sections) {
                html += this.renderSection(section);
            }

            html += '</div>';
        }

        container.innerHTML = html;

        // Initialize syntax highlighting if Prism is available
        if (typeof Prism !== 'undefined') {
            Prism.highlightAllUnder(container);
        }
    }

    /**
     * Render a single section
     */
    renderSection(section) {
        let html = '';

        if (section.type === 'theory') {
            html += `
                <div class="section theory-section">
                    <h2>${this.escapeHtml(section.title)}</h2>
                    <div class="content">
                        ${this.renderMarkdown(section.content)}
                    </div>
            `;

            // Render examples if present
            if (section.examples && section.examples.length > 0) {
                html += '<div class="examples">';
                section.examples.forEach((example, index) => {
                    html += `
                        <div class="example">
                            <h4>Örnek ${index + 1}: ${this.escapeHtml(example.title || '')}</h4>
                            <div class="example-content">
                                ${example.explanation ? `<p>${this.escapeHtml(example.explanation)}</p>` : ''}
                                <pre><code class="language-python">${this.escapeHtml(example.code)}</code></pre>
                                ${example.output ? `<div class="example-output"><strong>Çıktı:</strong>\n${this.escapeHtml(example.output)}</div>` : ''}
                            </div>
                        </div>
                    `;
                });
                html += '</div>';
            }

            html += '</div>';
        } else if (section.type === 'practice') {
            html += this.renderPracticeSection(section);
        }

        return html;
    }

    /**
     * Render practice/exercise section
     */
    renderPracticeSection(section) {
        const exercise = section.exercise || {};
        const testCases = exercise.test_cases || [];

        let html = `
            <div class="section practice-section">
                <h2>🎯 ${this.escapeHtml(section.title || 'Egzersiz')}</h2>
                <div class="exercise">
                    <div class="exercise-instructions">
                        ${this.renderMarkdown(exercise.instructions || '')}
                    </div>
        `;

        // Starter code
        if (exercise.starter_code) {
            html += `
                <div class="starter-code">
                    <h4>Başlangıç Kodu:</h4>
                    <pre><code class="language-python">${this.escapeHtml(exercise.starter_code)}</code></pre>
                </div>
            `;
        }

        // Hints
        if (exercise.hints && exercise.hints.length > 0) {
            html += '<div class="hints">';
            html += '<details>';
            html += '<summary>💡 İpuçları</summary>';
            html += '<ul>';
            exercise.hints.forEach((hint, index) => {
                html += `<li>${this.escapeHtml(hint)}</li>`;
            });
            html += '</ul>';
            html += '</details>';
            html += '</div>';
        }

        // Editor placeholder
        html += `
                    <div class="editor-container">
                        <div id="code-editor" class="code-editor"></div>
                    </div>
                    <div id="console-output" class="console-output" style="display: none;"></div>
                    <div class="editor-actions">
                        <button id="run-button" class="btn btn-primary">▶️ Kodu Çalıştır</button>
                        <button id="test-button" class="btn btn-success">✅ Testleri Çalıştır</button>
                        <button id="clear-button" class="btn btn-secondary">🗑️ Temizle</button>
                    </div>
        `;

        // Test cases info
        if (testCases.length > 0) {
            html += `
                <div class="test-info">
                    <h4>Test Çalışması (${testCases.length} test):</h4>
                    <p>Testleri çalıştır butonuna tıkla kodun tüm test vakalarını geçip geçmediğini görmek için.</p>
                </div>
            `;
        }

        html += `
                </div>
            </div>
        `;

        return html;
    }

    /**
     * Simple markdown to HTML conversion
     */
    renderMarkdown(markdown) {
        if (!markdown) return '';

        let html = markdown
            // Code blocks
            .replace(/```([a-z]*)\n([\s\S]*?)\n```/g, (match, lang, code) => {
                return `<pre><code class="language-${lang || 'python'}">${this.escapeHtml(code.trim())}</code></pre>`;
            })
            // Inline code
            .replace(/`([^`]+)`/g, (match, code) => {
                return `<code>${this.escapeHtml(code)}</code>`;
            })
            // Bold
            .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
            .replace(/__([^_]+)__/g, '<strong>$1</strong>')
            // Italic
            .replace(/\*([^*]+)\*/g, '<em>$1</em>')
            .replace(/_([^_]+)_/g, '<em>$1</em>')
            // Line breaks
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');

        return `<p>${html}</p>`;
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Get current lesson
     */
    getCurrentLesson() {
        return this.currentLesson;
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LessonRenderer;
}
