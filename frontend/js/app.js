/**
 * Main Application Controller
 * Orchestrates the entire learning platform
 */

class LearningApp {
    constructor() {
        this.api = new API();
        this.progressTracker = new ProgressTracker(this.api);
        this.lessonRenderer = new LessonRenderer();
        this.editor = null;
        this.currentView = 'home'; // home, lessons, lesson-detail
    }

    /**
     * Initialize the application
     */
    async init() {
        console.log('Initializing Learning Platform...');

        // Initialize dark mode
        this.initDarkMode();

        // Set up event listeners
        this.setupEventListeners();

        // Check API health
        const isHealthy = await this.api.healthCheck();
        if (!isHealthy) {
            this.showError('API bağlantısı başarısız. Lütfen sayfayı yenileyin.');
            return;
        }

        // Load initial data
        await this.loadInitialData();

        // Show home view initially
        this.showHomeView();

        console.log('Application initialized successfully');
    }

    /**
     * Initialize dark mode
     */
    initDarkMode() {
        // Check localStorage for saved preference
        const savedDarkMode = localStorage.getItem('darkMode');

        if (savedDarkMode === 'enabled') {
            document.body.classList.add('dark-mode');
        } else if (savedDarkMode === null) {
            // Check system preference
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.body.classList.add('dark-mode');
                localStorage.setItem('darkMode', 'enabled');
            }
        }
    }

    /**
     * Toggle dark mode
     */
    toggleDarkMode() {
        const isDarkMode = document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Navigation and actions
        document.addEventListener('click', (e) => {
            if (e.target.matches('[data-action="start-learning"]')) {
                e.preventDefault();
                this.showLessonsView();
            } else if (e.target.matches('[data-action="lesson-item"]')) {
                e.preventDefault();
                const lessonId = e.target.dataset.lessonId;
                this.showLessonDetailView(lessonId);
            } else if (e.target.matches('[data-action="back-to-lessons"]')) {
                e.preventDefault();
                this.showLessonsView();
            } else if (e.target.matches('#run-button')) {
                e.preventDefault();
                this.runCode();
            } else if (e.target.matches('#test-button')) {
                e.preventDefault();
                this.testExercise();
            } else if (e.target.matches('#clear-button')) {
                e.preventDefault();
                this.clearEditor();
            } else if (e.target.matches('[data-action="next-lesson"]')) {
                e.preventDefault();
                this.nextLesson();
            } else if (e.target.matches('[data-action="prev-lesson"]')) {
                e.preventDefault();
                this.previousLesson();
            } else if (e.target.matches('[data-action="toggle-dark-mode"]')) {
                e.preventDefault();
                this.toggleDarkMode();
                this.updateDarkModeButton();
            }
        });
    }

    /**
     * Update dark mode button icon
     */
    updateDarkModeButton() {
        const btn = document.querySelector('[data-action="toggle-dark-mode"]');
        if (btn) {
            const isDark = document.body.classList.contains('dark-mode');
            btn.innerHTML = isDark ? '☀️' : '🌙';
        }
    }

    /**
     * Get dark mode button HTML
     */
    getDarkModeButton() {
        const isDark = document.body.classList.contains('dark-mode');
        return `<button class="dark-mode-toggle" data-action="toggle-dark-mode" title="Karanlık mod">${isDark ? '☀️' : '🌙'}</button>`;
    }

    /**
     * Load initial data from API
     */
    async loadInitialData() {
        try {
            // Load lessons
            const lessons = await this.progressTracker.loadLessons();
            console.log(`Loaded ${lessons.length} lessons`);

            // Load progress
            const progress = await this.progressTracker.loadProgress();
            console.log('Progress loaded:', progress);

            // Set first lesson as current if not set
            if (!this.progressTracker.getCurrentLesson() && lessons.length > 0) {
                this.progressTracker.setCurrentLesson(lessons[0]);
            }
        } catch (error) {
            console.error('Error loading initial data:', error);
            this.showError('İlk veriler yüklenemedi. Lütfen sayfayı yenileyin.');
        }
    }

    /**
     * Show home view
     */
    showHomeView() {
        this.currentView = 'home';

        const app = document.getElementById('app');
        if (!app) return;

        const progress = this.progressTracker.formatProgress();

        app.innerHTML = `
            ${this.getDarkModeButton()}
            <div class="view-home">
                <div class="home-container">
                    <div class="home-header">
                        <h1>🐍 Python Öğrenme Platformu</h1>
                        <p>Python'un temellerinden ileri konulara kadar kapsamlı bir öğrenme yolu</p>
                    </div>

                    <div class="progress-section">
                        <div class="progress-card">
                            <h3>📊 Senin İlerlemen</h3>
                            <div class="progress-bar">
                                <div class="progress-fill" style="width: ${progress.percentage}%"></div>
                            </div>
                            <p class="progress-text">${progress.displayText}</p>
                        </div>
                    </div>

                    <div class="features-grid">
                        <div class="feature-card">
                            <h3>📚 56 Ders</h3>
                            <p>Temel sözdiziminden Turtle Graphics'e kadar</p>
                        </div>
                        <div class="feature-card">
                            <h3>💻 Canlı Kod Editörü</h3>
                            <p>Tarayıcıda Python kodu çalıştırın</p>
                        </div>
                        <div class="feature-card">
                            <h3>🎯 Egzersizler</h3>
                            <p>Her dersin ardından pratik alıştırmalar</p>
                        </div>
                        <div class="feature-card">
                            <h3>🚀 İnteraktif</h3>
                            <p>Kod yazın, çıktıyı hemen görün</p>
                        </div>
                    </div>

                    <button class="btn btn-large btn-primary" data-action="start-learning">
                        Öğrenmeye Başla →
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Show lessons list view
     */
    async showLessonsView() {
        this.currentView = 'lessons';

        const app = document.getElementById('app');
        if (!app) return;

        const lessons = this.progressTracker.getLessons();
        const progress = this.progressTracker.formatProgress();

        let lessonsHtml = '<div class="lessons-list">';
        lessons.forEach((lesson, index) => {
            lessonsHtml += `
                <div class="lesson-card" data-action="lesson-item" data-lesson-id="${lesson.id}" style="cursor: pointer;">
                    <div class="lesson-number">${lesson.order}</div>
                    <div class="lesson-info">
                        <h3>${this.escapeHtml(lesson.title)}</h3>
                        <p>${this.escapeHtml(lesson.description || '')}</p>
                    </div>
                    <div class="lesson-week">Hafta ${lesson.week}</div>
                </div>
            `;
        });
        lessonsHtml += '</div>';

        app.innerHTML = `
            ${this.getDarkModeButton()}
            <div class="view-lessons">
                <div class="lessons-header">
                    <h2>Tüm Dersler</h2>
                    <p>${progress.displayText}</p>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${progress.percentage}%"></div>
                </div>
                ${lessonsHtml}
            </div>
        `;
    }

    /**
     * Show lesson detail view
     */
    async showLessonDetailView(lessonId) {
        this.currentView = 'lesson-detail';

        try {
            const result = await this.api.getLesson(lessonId);

            if (!result.success) {
                this.showError('Ders yüklenemedi');
                return;
            }

            const lesson = result.lesson;
            this.progressTracker.setCurrentLesson(lesson);

            const app = document.getElementById('app');
            if (!app) return;

            app.innerHTML = `
                ${this.getDarkModeButton()}
                <div class="view-lesson-detail">
                    <div class="lesson-toolbar">
                        <button class="btn btn-sm" data-action="back-to-lessons">← Geri Dön</button>
                        <div class="lesson-nav">
                            <button class="btn btn-sm" data-action="prev-lesson" ${!this.progressTracker.getPreviousLesson() ? 'disabled' : ''}>Önceki</button>
                            <span class="lesson-title">${this.escapeHtml(lesson.title)}</span>
                            <button class="btn btn-sm" data-action="next-lesson" ${!this.progressTracker.getNextLesson() ? 'disabled' : ''}>Sonraki</button>
                        </div>
                    </div>
                    <div id="lesson-content"></div>
                </div>
            `;

            // Render lesson content
            await this.lessonRenderer.renderLesson(lesson, 'lesson-content');

            // Initialize editor if there's a practice section
            const editorContainer = document.getElementById('code-editor');
            if (editorContainer && lesson.sections) {
                const practiceSection = lesson.sections.find(s => s.type === 'practice');
                if (practiceSection) {
                    this.editor = new CodeEditor('code-editor', {
                        height: '400px',
                        initialContent: practiceSection.exercise?.starter_code || ''
                    });
                }
            }

            // Highlight code blocks
            if (typeof Prism !== 'undefined') {
                Prism.highlightAll();
            }
        } catch (error) {
            console.error('Error loading lesson:', error);
            this.showError('Ders yüklenirken hata oluştu');
        }
    }

    /**
     * Run code in editor
     */
    async runCode() {
        if (!this.editor) return;

        try {
            const lesson = this.progressTracker.getCurrentLesson();
            const result = await this.editor.run(this.api, lesson?.id);
        } catch (error) {
            console.error('Error running code:', error);
        }
    }

    /**
     * Test exercise
     */
    async testExercise() {
        if (!this.editor) return;

        try {
            const lesson = this.progressTracker.getCurrentLesson();
            const practiceSection = lesson.sections?.find(s => s.type === 'practice');
            const exercise = practiceSection?.exercise;

            if (!exercise || !exercise.test_cases) {
                alert('Bu egzersiz için test yapılamaz');
                return;
            }

            const result = await this.editor.test(
                this.api,
                exercise.id,
                exercise.test_cases,
                lesson.id
            );

            if (result && result.success) {
                alert('🎉 Tebrikler! Tüm testler başarılı!');
                // Mark lesson as complete
                await this.progressTracker.markLessonComplete(lesson.id);
            }
        } catch (error) {
            console.error('Error testing exercise:', error);
        }
    }

    /**
     * Clear editor
     */
    clearEditor() {
        if (this.editor) {
            if (confirm('Editörü temizlemek istediğinize emin misiniz?')) {
                this.editor.clear();
                this.editor.clearOutput();
            }
        }
    }

    /**
     * Navigate to next lesson
     */
    async nextLesson() {
        const nextLesson = this.progressTracker.getNextLesson();
        if (nextLesson) {
            await this.showLessonDetailView(nextLesson.id);
        }
    }

    /**
     * Navigate to previous lesson
     */
    async previousLesson() {
        const prevLesson = this.progressTracker.getPreviousLesson();
        if (prevLesson) {
            await this.showLessonDetailView(prevLesson.id);
        }
    }

    /**
     * Show error message
     */
    showError(message) {
        const app = document.getElementById('app');
        if (app) {
            app.innerHTML = `
                <div class="error-message">
                    <h2>❌ Hata</h2>
                    <p>${this.escapeHtml(message)}</p>
                    <button class="btn btn-primary" onclick="location.reload()">Sayfayı Yenile</button>
                </div>
            `;
        }
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
    window.app = new LearningApp();
    await window.app.init();
});
