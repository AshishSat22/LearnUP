# 🎓 LearnUP — The Ultimate Class 12 CBSE Learning Portal

**LearnUP** is a meticulously engineered, fully offline-capable web application designed to revolutionize board exam preparation for Class 12 CBSE students. Originally conceived as a lightweight Tkinter desktop application, LearnUP has been radically reimagined from the ground up into a high-performance **Flask-powered Web App** featuring a breathtaking, responsive UI, zero-dependency data architecture, and a suite of advanced procedural generation engines.

### 🚀 Technical Marvels & Core Features
- **Stunning Glassmorphism UI**: Built entirely without heavy frontend frameworks, LearnUP utilizes pure Vanilla CSS, flexbox geometries, and native CSS variables to achieve buttery-smooth micro-animations, glassmorphism cards, and an instantaneous system-wide Light/Dark mode toggle.
- **Live YouTube Linking Engine**: Why settle for generic links? LearnUP features a custom Python live-scraper that actively searches and natively embeds the exact top-performing educational videos from industry leaders like **Physics Wallah**, **Unacademy**, and **Apni Kaksha** for over 900 syllabus topics across Physics, Chemistry, and Maths.
- **Offline Video Portability**: Designed for students with limited internet access, every video module securely falls back to a custom HTML5 `<video>` engine equipped with one-click "Download Offline" direct mp4 saving. 
- **SymPy-Powered Procedural SYQs**: Moving far beyond static text files, LearnUP utilizes the `SymPy` mathematics library to dynamically generate over 12,000 highly accurate, interactive flashcard-style past year questions (PYQs). It automatically derives specific numerical values, thermodynamic states, and step-by-step calculus integration proofs on-the-fly.
- **Authentic CBSE PDF Engine**: A massive internal archive powered by a local 6-year CBSE data pipeline (2018–2024) allows students to practice using a custom-built Dual-Pane Native PDF Viewer, aligning authentic Sample Question Papers exactly alongside their Official Marking Schemes.
- **Rich Interactive Tooling**: Complete with a localized JSON-based Bookmark architecture, weighted marking categories (1-mark to 5-mark toggles), comprehensive Quiz analytics, and global topic indexing.

Whether you are here to explore Python Flask integration, admire advanced CSS aesthetics, or study CBSE Class 12 board preparations, LearnUP stands as a complete, self-contained educational powerhouse.

### ⚙️ Installation & Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/LearnUP.git
   cd LearnUP
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate the robust local database of questions, videos, and papers (Optional, but recommended for full functionality):
   ```bash
   python generate_data.py
   python expand_physics_maths.py
   python expand_chemistry.py
   python expand_videos.py
   python expand_pyqs.py
   python download_sqps.py
   python setup_offline_videos.py
   ```

4. Run the application:
   ```bash
   python app_web.py
   ```

5. Open your web browser and navigate to `http://127.0.0.1:5000/`.
