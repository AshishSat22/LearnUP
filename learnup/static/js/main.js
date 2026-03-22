document.addEventListener('DOMContentLoaded', () => {
    // Theme logic
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.getElementById('app-body');
    
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        body.classList.replace('light-mode', 'dark-mode');
        themeToggle.textContent = '☀️';
    }

    themeToggle.addEventListener('click', () => {
        if (body.classList.contains('light-mode')) {
            body.classList.replace('light-mode', 'dark-mode');
            themeToggle.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.replace('dark-mode', 'light-mode');
            themeToggle.textContent = '🌙';
            localStorage.setItem('theme', 'light');
        }
    });

    // Bookmark Toggle logic
    const bookmarkBtns = document.querySelectorAll('.bookmark-btn');
    bookmarkBtns.forEach(btn => {
        btn.addEventListener('click', async (e) => {
            const btype = btn.dataset.type;
            const subject = btn.dataset.subject;
            const chapter = btn.dataset.chapter;
            const title = btn.dataset.title;
            const url = btn.dataset.url || "";

            try {
                const res = await fetch('/api/toggle_bookmark', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: btype, subject, chapter, title, url })
                });
                const data = await res.json();
                if (data.success) {
                    btn.classList.toggle('active');
                    btn.textContent = data.added ? '🔖 Saved' : '🔖 Bookmark';
                    if (data.added) {
                        btn.style.color = "var(--accent)";
                    } else {
                        btn.style.color = "inherit";
                    }
                }
            } catch (err) {
                console.error("Failed to toggle bookmark", err);
            }
        });
    });
});
