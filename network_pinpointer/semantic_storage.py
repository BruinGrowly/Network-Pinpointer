#!/usr/bin/env python3
"""
Semantic Storage - Persistent Storage for Semantic Profiles

Provides SQLite-based storage for semantic profiles, baselines, and history.
Enables drift detection, trend analysis, and historical queries.
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from dataclasses import asdict

from .semantic_probe import SemanticProfile
from .semantic_engine import Coordinates


class SemanticStorage:
    """Persistent storage for semantic profiles and history"""
    
    DEFAULT_DB_PATH = os.path.expanduser("~/.network-pinpointer/semantic.db")
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or self.DEFAULT_DB_PATH
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        db_dir = os.path.dirname(self.db_path)
        Path(db_dir).mkdir(parents=True, exist_ok=True)
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT NOT NULL,
                ip_address TEXT,
                timestamp DATETIME NOT NULL,
                love REAL,
                justice REAL,
                power REAL,
                wisdom REAL,
                dominant_dimension TEXT,
                harmony_score REAL,
                semantic_clarity REAL,
                semantic_mass REAL,
                archetype TEXT,
                archetype_confidence REAL,
                service_classification TEXT,
                security_posture TEXT,
                inferred_purpose TEXT,
                open_ports TEXT,
                scan_duration REAL,
                is_baseline BOOLEAN DEFAULT 0
            )
        ''')
        
        # ... (indices) ...

    def store_profile(self, profile: SemanticProfile, is_baseline: bool = False):
        """Store a semantic profile"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Extract archetype info
        archetype_name = None
        archetype_confidence = None
        if profile.matched_archetypes:
            archetype_name = profile.matched_archetypes[0][0].name
            archetype_confidence = profile.matched_archetypes[0][1]
        
        # Convert open ports to JSON
        open_ports_json = json.dumps([p.port for p in profile.open_ports if p.is_open])
        
        cursor.execute('''
            INSERT INTO profiles (
                target, ip_address, timestamp,
                love, justice, power, wisdom,
                dominant_dimension, harmony_score, semantic_clarity, semantic_mass,
                archetype, archetype_confidence,
                service_classification, security_posture, inferred_purpose,
                open_ports, scan_duration, is_baseline
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            profile.target,
            profile.ip_address,
            profile.timestamp.isoformat(),
            profile.ljpw_coordinates.love if profile.ljpw_coordinates else None,
            profile.ljpw_coordinates.justice if profile.ljpw_coordinates else None,
            profile.ljpw_coordinates.power if profile.ljpw_coordinates else None,
            profile.ljpw_coordinates.wisdom if profile.ljpw_coordinates else None,
            profile.dominant_dimension,
            profile.harmony_score,
            profile.semantic_clarity,
            getattr(profile, 'semantic_mass', 0.0), # Handle missing mass
            archetype_name,
            archetype_confidence,
            profile.service_classification,
            profile.security_posture,
            profile.inferred_purpose,
            open_ports_json,
            profile.scan_duration,
            1 if is_baseline else 0
        ))
        
        conn.commit()
        conn.close()
    
    def get_profile(self, target: str, timestamp: datetime = None) -> Optional[Dict]:
        """Retrieve profile for target at specific time (or latest)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if timestamp:
            cursor.execute('''
                SELECT * FROM profiles 
                WHERE target = ? AND timestamp <= ?
                ORDER BY timestamp DESC LIMIT 1
            ''', (target, timestamp.isoformat()))
        else:
            cursor.execute('''
                SELECT * FROM profiles 
                WHERE target = ?
                ORDER BY timestamp DESC LIMIT 1
            ''', (target,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_dict(cursor, row)
    
    def get_profile_history(
        self, 
        target: str, 
        hours: int = 24,
        limit: int = 1000
    ) -> List[Dict]:
        """Get all profiles for target in time range"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
            SELECT * FROM profiles 
            WHERE target = ? AND timestamp >= ?
            ORDER BY timestamp DESC LIMIT ?
        ''', (target, since.isoformat(), limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_dict(cursor, row) for row in rows]
    
    def get_baseline(self, target: str) -> Optional[Dict]:
        """Get baseline profile for target"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM profiles 
            WHERE target = ? AND is_baseline = 1
            ORDER BY timestamp DESC LIMIT 1
        ''', (target,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_dict(cursor, row)
    
    def set_baseline(self, target: str, profile_id: int = None):
        """Set baseline profile for target"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clear existing baselines for this target
        cursor.execute('''
            UPDATE profiles SET is_baseline = 0 WHERE target = ?
        ''', (target,))
        
        # Set new baseline
        if profile_id:
            cursor.execute('''
                UPDATE profiles SET is_baseline = 1 WHERE id = ?
            ''', (profile_id,))
        else:
            # Use most recent profile
            cursor.execute('''
                UPDATE profiles SET is_baseline = 1 
                WHERE id = (
                    SELECT id FROM profiles 
                    WHERE target = ? 
                    ORDER BY timestamp DESC LIMIT 1
                )
            ''', (target,))
        
        conn.commit()
        conn.close()
    
    def get_all_targets(self) -> List[str]:
        """Get list of all monitored targets"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT target FROM profiles ORDER BY target
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]
    
    def get_targets_with_baselines(self) -> List[str]:
        """Get list of targets that have baselines set"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DISTINCT target FROM profiles 
            WHERE is_baseline = 1 
            ORDER BY target
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        return [row[0] for row in rows]
    
    def delete_target_history(self, target: str, keep_baseline: bool = True):
        """Delete history for target (optionally keeping baseline)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if keep_baseline:
            cursor.execute('''
                DELETE FROM profiles
                WHERE target = ? AND is_baseline = 0
            ''', (target,))
        else:
            cursor.execute('''
                DELETE FROM profiles WHERE target = ?
            ''', (target,))

        conn.commit()
        conn.close()

    def clear_baseline(self, target: str):
        """Clear baseline flag for a target (removes baseline status)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE profiles SET is_baseline = 0 WHERE target = ?
        ''', (target,))

        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM profiles')
        total_profiles = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT target) FROM profiles')
        total_targets = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM profiles WHERE is_baseline = 1')
        total_baselines = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT MIN(timestamp), MAX(timestamp) FROM profiles
        ''')
        date_range = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_profiles': total_profiles,
            'total_targets': total_targets,
            'total_baselines': total_baselines,
            'oldest_profile': date_range[0],
            'newest_profile': date_range[1],
            'db_path': self.db_path,
        }
    
    def _row_to_dict(self, cursor, row) -> Dict:
        """Convert database row to dictionary"""
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))
    
    def dict_to_coordinates(self, profile_dict: Dict) -> Optional[Coordinates]:
        """Convert profile dict to Coordinates object"""
        if not all(k in profile_dict for k in ['love', 'justice', 'power', 'wisdom']):
            return None

        # Handle None values by defaulting to 0.0
        return Coordinates(
            love=profile_dict['love'] or 0.0,
            justice=profile_dict['justice'] or 0.0,
            power=profile_dict['power'] or 0.0,
            wisdom=profile_dict['wisdom'] or 0.0
        )
