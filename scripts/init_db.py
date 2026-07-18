import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import app
from portfolio.extensions import db
from portfolio.models import Experience, Profile, Project, Skill, User

HERO_URL = "/images/default-hero.jpg"
ABOUT_URL = "/images/default-about.jpg"
PROJECT_IMAGES = [
    "/images/default-project-1.jpg",
    "/images/default-project-2.jpg",
    "/images/default-project-3.jpg",
]


def seed_admin():
    email = os.getenv("ADMIN_EMAIL", "admin@portfolio.local").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "GantiPasswordKuat123!")
    if len(password) < 10:
        raise ValueError("ADMIN_PASSWORD minimal 10 karakter.")
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        print(f"Admin dibuat: {email}")


def seed_profile():
    if Profile.query.first():
        return
    db.session.add(Profile(
        brand_name="DevPortfolio",
        full_name="Nama Lengkap",
        headline="Web Developer & UI/UX Enthusiast",
        short_intro="I specialize in building functional, aesthetic, and user-centric web applications that bridge the gap between complex code and intuitive design.",
        availability_text="Available for freelance",
        about_text="I'm a passionate creator who lives at the intersection of aesthetic design and logical structure. With a background in both Computer Science and Graphic Design, I approach every project as a puzzle to be solved beautifully.",
        about_text_secondary="My goal is to build digital products that not only perform exceptionally well but also tell a story and delight users through thoughtful interaction and visual harmony.",
        years_experience="5+",
        email="hello@devportfolio.com",
        phone="+62 812 3456 789",
        location="Jakarta, Indonesia",
        education="Bachelor of CS",
        work_status="Open for Work",
        github_url="https://github.com/",
        linkedin_url="https://www.linkedin.com/",
        hero_image_url=HERO_URL,
        about_image_url=ABOUT_URL,
        footer_text="Web Developer & UI/UX Enthusiast",
    ))


def seed_skills():
    if Skill.query.count():
        return
    data = [
        ("Frontend", "code", "HTML / CSS / JS\nReact & Next.js\nTailwind CSS"),
        ("Backend", "settings_ethernet", "Flask (Python)\nLaravel (PHP)\nNode.js"),
        ("Database", "database", "MySQL\nPostgreSQL\nMongoDB"),
        ("Design", "brush", "Figma\nAdobe XD\nUI Prototyping"),
        ("Tools", "construction", "Git & GitHub\nCloudinary\nVercel / AWS"),
    ]
    for order, (category, icon, items) in enumerate(data, 1):
        db.session.add(Skill(category=category, icon=icon, items=items, sort_order=order))


def seed_experiences():
    if Experience.query.count():
        return
    data = [
        ("2022 - Present", "Senior UI/UX Developer", "TechNova Solutions", "Leading the frontend architectural decisions and design systems for enterprise-grade SaaS platforms. Mentoring junior developers and bridging the gap between stakeholders and engineering.", True),
        ("2020 - 2022", "Fullstack Developer", "Creative Digital Agency", "Developed custom web solutions for high-profile clients using React and Laravel. Focused on high-performance animations and responsive layouts.", False),
        ("2016 - 2020", "B.S. Computer Science", "University of Technology", "Graduated with honors. Focused on Web Technologies and Human-Computer Interaction.", False),
    ]
    for order, (period, title, org, description, active) in enumerate(data, 1):
        db.session.add(Experience(period=period, title=title, organization=org, description=description, item_type="education" if order == 3 else "experience", sort_order=order, is_active=active))


def seed_projects():
    if Project.query.count():
        return
    data = [
        ("Vortex Dashboard", "A comprehensive financial tracking system with real-time data visualization and secure API integration.", "Next.js\nTailwind", PROJECT_IMAGES[0]),
        ("Aura Commerce", "Modern headless e-commerce solution focused on extreme performance and minimal user friction.", "React\nNode.js", PROJECT_IMAGES[1]),
        ("Nova Portfolio", "An immersive 3D-infused portfolio for a creative agency, pushing the boundaries of web interactions.", "Figma\nThree.js", PROJECT_IMAGES[2]),
    ]
    for order, (title, description, technologies, image_url) in enumerate(data, 1):
        db.session.add(Project(title=title, description=description, technologies=technologies, image_url=image_url, live_url="https://example.com", code_url="https://github.com/", is_featured=True, sort_order=order))


with app.app_context():
    db.create_all()
    seed_admin()
    seed_profile()
    seed_skills()
    seed_experiences()
    seed_projects()
    db.session.commit()
    print("Database dan data awal berhasil disiapkan.")
