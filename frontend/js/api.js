/**
 * API Client for Python Learning Platform
 * Handles all communication with the backend
 */

class API {
    constructor(baseURL = null) {
        // Use current domain for API
        if (!baseURL) {
            const protocol = window.location.protocol;
            const host = window.location.host;
            baseURL = `${protocol}//${host}`;
        }
        this.baseURL = baseURL;
        this.apiURL = `${baseURL}/api`;
    }

    // ==================== Lessons ====================
    async getLessons() {
        try {
            const response = await fetch(`${this.apiURL}/lessons`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to load lessons');
            return data;
        } catch (error) {
            console.error('Error fetching lessons:', error);
            throw error;
        }
    }

    async getLesson(lessonId) {
        try {
            const response = await fetch(`${this.apiURL}/lessons/${lessonId}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to load lesson');
            return data;
        } catch (error) {
            console.error(`Error fetching lesson ${lessonId}:`, error);
            throw error;
        }
    }

    async completeLesson(lessonId) {
        try {
            const response = await fetch(`${this.apiURL}/lessons/${lessonId}/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to complete lesson');
            return data;
        } catch (error) {
            console.error(`Error completing lesson ${lessonId}:`, error);
            throw error;
        }
    }

    // ==================== Code Execution ====================
    async executeCode(code, lessonId = null, exerciseId = null) {
        try {
            const response = await fetch(`${this.apiURL}/execute`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code,
                    lesson_id: lessonId,
                    exercise_id: exerciseId
                })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to execute code');
            return data;
        } catch (error) {
            console.error('Error executing code:', error);
            throw error;
        }
    }

    async testExercise(exerciseId, code, testCases, lessonId = null) {
        try {
            const response = await fetch(`${this.apiURL}/exercises/${exerciseId}/test`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code,
                    test_cases: testCases,
                    lesson_id: lessonId
                })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to test exercise');
            return data;
        } catch (error) {
            console.error('Error testing exercise:', error);
            throw error;
        }
    }

    // ==================== Progress ====================
    async getProgress() {
        try {
            const response = await fetch(`${this.apiURL}/progress`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to load progress');
            return data;
        } catch (error) {
            console.error('Error fetching progress:', error);
            throw error;
        }
    }

    // ==================== Health Check ====================
    async healthCheck() {
        try {
            const response = await fetch(`${this.apiURL}/health`);
            const data = await response.json();
            return response.ok;
        } catch (error) {
            console.error('Health check failed:', error);
            return false;
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
