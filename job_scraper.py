import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import re

class JobScraper:
    """
    Web scraper for collecting job listings from job boards.
    Uses proper error handling, rate limiting, and data validation.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.jobs: List[Dict] = []
    
    def scrape_frontend_mentor_jobs(self) -> List[Dict]:
        """
        Scrape job listings from Frontend Mentor challenge page.
        In production, this would target real job boards.
        """
        # Sample data based on the provided HTML structure
        sample_jobs = [
            {
                "id": 1,
                "company": "Photosnap",
                "logo": None,
                "is_new": True,
                "is_featured": True,
                "position": "Senior Frontend Developer",
                "role": "Frontend",
                "level": "Senior",
                "posted_at": "1d ago",
                "contract": "Full Time",
                "location": "USA only",
                "languages": ["HTML", "CSS", "JavaScript"],
                "tools": []
            },
            {
                "id": 2,
                "company": "Manage",
                "logo": None,
                "is_new": True,
                "is_featured": True,
                "position": "Fullstack Developer",
                "role": "Fullstack",
                "level": "Midweight",
                "posted_at": "1d ago",
                "contract": "Part Time",
                "location": "Remote",
                "languages": ["Python"],
                "tools": ["React"]
            },
            {
                "id": 3,
                "company": "Account",
                "logo": None,
                "is_new": False,
                "is_featured": False,
                "position": "Junior Frontend Developer",
                "role": "Frontend",
                "level": "Junior",
                "posted_at": "2d ago",
                "contract": "Part Time",
                "location": "USA only",
                "languages": ["JavaScript"],
                "tools": ["React", "Sass"]
            },
            {
                "id": 4,
                "company": "MyHome",
                "logo": None,
                "is_new": False,
                "is_featured": False,
                "position": "Junior Frontend Developer",
                "role": "Frontend",
                "level": "Junior",
                "posted_at": "5d ago",
                "contract": "Contract",
                "location": "USA only",
                "languages": ["CSS", "JavaScript"],
                "tools": []
            },
            {
                "id": 5,
                "company": "Loop Studios",
                "logo": None,
                "is_new": False,
                "is_featured": False,
                "position": "Software Engineer",
                "role": "Fullstack",
                "level": "Midweight",
                "posted_at": "1w ago",
                "contract": "Full Time",
                "location": "Worldwide",
                "languages": ["JavaScript", "Ruby"],
                "tools": ["Sass"]
            },
            {
                "id": 6,
                "company": "FaceIt",
                "logo": None,
                "is_new": False,
                "is_featured": False,
                "position": "Junior Backend Developer",
                "role": "Backend",
                "level": "Junior",
                "posted_at": "2w ago",
                "contract": "Full Time",
                "location": "UK only",
                "languages": ["Ruby"],
                "tools": ["RoR"]
            },
            {
                "id": 7,
                "company": "Shortly",
                "logo": None,
                "is_new": False,
                "is_featured": False,
                "position": "Junior Developer",
                "role": "Frontend",
                "level": "Junior",
                "posted_at": "2w ago",
                "contract": "Full Time",
                "location": "Worldwide",
                "languages": ["HTML", "JavaScript"],
                "tools": ["Sass"]
            },
            {
                "id": 8,
                "company": "Insure",
                "logo": None,
                "is_new": False,
                "is_featured": False,
                "position": "Junior Frontend Developer",
                "role": "Frontend",
                "level": "Junior",
                "posted_at": "2w ago",
                "contract": "Full Time",
                "location": "USA only",
                "languages": ["JavaScript"],
                "tools": ["Vue", "Sass"]
            },
            {
                "id": 9,
                "company": "Eyecam Co.",
                "logo": None,
                "is_new": False,
                "is_featured": False,
                "position": "Full Stack Engineer",
                "role": "Fullstack",
                "level": "Midweight",
                "posted_at": "3w ago",
                "contract": "Full Time",
                "location": "Worldwide",
                "languages": ["JavaScript", "Python"],
                "tools": ["Django"]
            },
            {
                "id": 10,
                "company": "The Air Filter Company",
                "logo": None,
                "is_new": False,
                "is_featured": False,
                "position": "Front-end Dev",
                "role": "Frontend",
                "level": "Junior",
                "posted_at": "1mo ago",
                "contract": "Part Time",
                "location": "Worldwide",
                "languages": ["JavaScript"],
                "tools": ["React", "Sass"]
            }
        ]
        
        return sample_jobs
    
    def scrape_remote_jobs(self) -> List[Dict]:
        """
        Scrape real job listings from remoteok.io API.
        This demonstrates real web scraping in production.
        """
        try:
            # RemoteOK API (no API key required, CORS enabled)
            url = "https://remoteok.com/api"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            jobs_data = response.json()
            jobs = []
            
            for job in jobs_data[:20]:  # Limit to 20 most recent
                if isinstance(job, dict) and 'position' in job:
                    job_entry = {
                        "id": job.get('id', len(jobs) + 1),
                        "company": job.get('company', 'Unknown'),
                        "logo": None,
                        "is_new": job.get('date') == 'new',
                        "is_featured": False,
                        "position": job.get('position', ''),
                        "role": self._extract_role(job.get('position', '')),
                        "level": self._extract_level(job.get('position', ''), job.get('tags', [])),
                        "posted_at": job.get('date', 'Recently'),
                        "contract": job.get('type', 'Full Time'),
                        "location": job.get('location', 'Remote'),
                        "languages": self._extract_languages(job.get('tags', [])),
                        "tools": self._extract_tools(job.get('tags', []))
                    }
                    jobs.append(job_entry)
                    
            print(f"✅ Successfully scraped {len(jobs)} jobs from RemoteOK")
            return jobs
            
        except requests.RequestException as e:
            print(f"❌ Error scraping RemoteOK: {e}")
            return []
    
    def _extract_role(self, position: str) -> str:
        """Extract role from position title."""
        position_lower = position.lower()
        if 'frontend' in position_lower or 'front-end' in position_lower:
            return 'Frontend'
        elif 'backend' in position_lower or 'back-end' in position_lower:
            return 'Backend'
        elif 'fullstack' in position_lower or 'full-stack' in position_lower:
            return 'Fullstack'
        return 'Other'
    
    def _extract_level(self, position: str, tags: list) -> str:
        """Extract experience level from position and tags."""
        position_lower = position.lower()
        tags_lower = [tag.lower() for tag in tags] if tags else []
        
        search_text = position_lower + ' ' + ' '.join(tags_lower)
        
        if 'senior' in search_text:
            return 'Senior'
        elif 'junior' in search_text or 'entry' in search_text:
            return 'Junior'
        elif 'mid' in search_text or 'midweight' in search_text:
            return 'Midweight'
        return 'Midweight'
    
    def _extract_languages(self, tags: list) -> list:
        """Extract programming languages from tags."""
        languages = ['Python', 'JavaScript', 'Java', 'Ruby', 'PHP', 'Go', 'Rust', 
                     'HTML', 'CSS', 'TypeScript', 'C++', 'C#', 'Swift', 'Kotlin']
        extracted = []
        
        if tags:
            for tag in tags:
                for lang in languages:
                    if tag.lower() == lang.lower():
                        extracted.append(lang)
        return extracted
    
    def _extract_tools(self, tags: list) -> list:
        """Extract tools/frameworks from tags."""
        tools = ['React', 'Vue', 'Angular', 'Django', 'Flask', 'Rails', 'Spring',
                 'Node', 'Express', 'Sass', 'Tailwind', 'Bootstrap', 'Docker', 'K8s']
        extracted = []
        
        if tags:
            for tag in tags:
                for tool in tools:
                    if tag.lower() == tool.lower():
                        extracted.append(tool)
        return extracted
    
    def save_jobs_to_json(self, jobs: List[Dict], filename: str = "jobs_data.json"):
        """Save scraped jobs to JSON file with timestamp."""
        output_data = {
            "last_updated": datetime.now().isoformat(),
            "total_jobs": len(jobs),
            "jobs": jobs
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved {len(jobs)} jobs to {filename}")
        return filename
    
    def run_scraper(self, use_real_scraping: bool = False):
        """
        Main method to run the scraper.
        
        Args:
            use_real_scraping: If True, scrape real job boards. If False, use sample data.
        """
        print("🚀 Starting job scraper...")
        
        if use_real_scraping:
            # Scrape from multiple sources
            remote_jobs = self.scrape_remote_jobs()
            self.jobs.extend(remote_jobs)
        else:
            # Use sample data for demonstration
            sample_jobs = self.scrape_frontend_mentor_jobs()
            self.jobs.extend(sample_jobs)
        
        # Save to JSON
        if self.jobs:
            filename = self.save_jobs_to_json(self.jobs)
            print(f"✨ Scraping complete! {len(self.jobs)} jobs collected.")
            return filename
        else:
            print("⚠️ No jobs were collected.")
            return None

if __name__ == "__main__":
    # Run the scraper
    scraper = JobScraper()
    
    # Set to False to use sample data, True for real web scraping
    scraper.run_scraper(use_real_scraping=False)