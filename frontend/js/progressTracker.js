/**
 * Progress Tracker
 * Manages user progress and state
 */

class ProgressTracker {
    constructor(api) {
        this.api = api;
        this.progress = null;
        this.lessons = [];
        this.currentLesson = null;
        this.storageKey = 'py-learning-progress';

        this.loadFromStorage();
    }

    /**
     * Load progress from API
     */
    async loadProgress() {
        try {
            const result = await this.api.getProgress();
            if (result.success) {
                this.progress = result.progress;
                this.saveToStorage();
                return this.progress;
            }
        } catch (error) {
            console.error('Error loading progress:', error);
        }
        return null;
    }

    /**
     * Load all lessons
     */
    async loadLessons() {
        try {
            const result = await this.api.getLessons();
            if (result.success) {
                this.lessons = result.lessons || [];
                this.saveToStorage();
                return this.lessons;
            }
        } catch (error) {
            console.error('Error loading lessons:', error);
        }
        return [];
    }

    /**
     * Get all lessons
     */
    getLessons() {
        return this.lessons;
    }

    /**
     * Get lesson by ID
     */
    getLessonById(lessonId) {
        return this.lessons.find(lesson => lesson.id === lessonId);
    }

    /**
     * Get current lesson
     */
    getCurrentLesson() {
        return this.currentLesson;
    }

    /**
     * Set current lesson
     */
    setCurrentLesson(lesson) {
        this.currentLesson = lesson;
        this.saveToStorage();
    }

    /**
     * Get next lesson
     */
    getNextLesson() {
        if (!this.currentLesson) return null;

        const currentIndex = this.lessons.findIndex(l => l.id === this.currentLesson.id);
        if (currentIndex >= 0 && currentIndex < this.lessons.length - 1) {
            return this.lessons[currentIndex + 1];
        }
        return null;
    }

    /**
     * Get previous lesson
     */
    getPreviousLesson() {
        if (!this.currentLesson) return null;

        const currentIndex = this.lessons.findIndex(l => l.id === this.currentLesson.id);
        if (currentIndex > 0) {
            return this.lessons[currentIndex - 1];
        }
        return null;
    }

    /**
     * Mark lesson as complete
     */
    async markLessonComplete(lessonId) {
        try {
            const result = await this.api.completeLesson(lessonId);
            if (result.success) {
                this.progress = result.progress;
                this.saveToStorage();
                return true;
            }
        } catch (error) {
            console.error('Error marking lesson complete:', error);
        }
        return false;
    }

    /**
     * Get progress percentage
     */
    getProgressPercentage() {
        return this.progress ? this.progress.percentage : 0;
    }

    /**
     * Get completed lessons count
     */
    getCompletedCount() {
        return this.progress ? this.progress.completed : 0;
    }

    /**
     * Get total lessons count
     */
    getTotalCount() {
        return this.progress ? this.progress.total : 0;
    }

    /**
     * Is lesson completed
     */
    isLessonCompleted(lessonId) {
        // This would require storing individual lesson completion status
        // For now, just check if it's before or equal to the completed count
        return false;
    }

    /**
     * Save state to localStorage for offline access
     */
    saveToStorage() {
        const data = {
            lessons: this.lessons,
            progress: this.progress,
            currentLesson: this.currentLesson,
            timestamp: new Date().toISOString()
        };
        localStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    /**
     * Load state from localStorage
     */
    loadFromStorage() {
        try {
            const data = JSON.parse(localStorage.getItem(this.storageKey));
            if (data) {
                this.lessons = data.lessons || [];
                this.progress = data.progress || null;
                this.currentLesson = data.currentLesson || null;
            }
        } catch (error) {
            console.error('Error loading from storage:', error);
        }
    }

    /**
     * Clear all stored data
     */
    clearStorage() {
        localStorage.removeItem(this.storageKey);
        this.lessons = [];
        this.progress = null;
        this.currentLesson = null;
    }

    /**
     * Format progress for display
     */
    formatProgress() {
        const completed = this.getCompletedCount();
        const total = this.getTotalCount();
        const percentage = this.getProgressPercentage();

        return {
            completed,
            total,
            percentage: Math.round(percentage),
            displayText: `${completed}/${total} tamamlandı (%${Math.round(percentage)})`
        };
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProgressTracker;
}
