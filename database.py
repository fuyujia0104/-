
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
from config import settings

class DatabaseManager:
    """数据库管理类，处理用户感官标记的存储和查询"""

    def __init__(self):
        self.db_path = settings.DATABASE_PATH
        self._init_db()

    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """初始化数据库表结构"""
        # 确保数据目录存在
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 创建感官标记表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sensory_marks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    address TEXT,
                    quietness INTEGER CHECK(quietness >= 1 AND quietness <= 5),
                    smell TEXT,
                    atmosphere TEXT,
                    best_season TEXT,
                    best_time_of_day TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 创建地点表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS places (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    name TEXT NOT NULL,
                    address TEXT,
                    place_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 创建地点与感官标记的关联表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS place_marks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    place_id INTEGER NOT NULL,
                    mark_id INTEGER NOT NULL,
                    FOREIGN KEY (place_id) REFERENCES places(id),
                    FOREIGN KEY (mark_id) REFERENCES sensory_marks(id)
                )
            """)

            conn.commit()

    def add_sensory_mark(self, mark_data: Dict[str, Any]) -> int:
        """添加感官标记"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sensory_marks (
                    latitude, longitude, address, quietness, smell, 
                    atmosphere, best_season, best_time_of_day, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                mark_data.get("latitude"),
                mark_data.get("longitude"),
                mark_data.get("address"),
                mark_data.get("quietness"),
                mark_data.get("smell"),
                mark_data.get("atmosphere"),
                mark_data.get("best_season"),
                mark_data.get("best_time_of_day"),
                mark_data.get("notes")
            ))
            conn.commit()
            return cursor.lastrowid

    def get_nearby_marks(self, lat: float, lon: float, radius_km: float = 1.0) -> List[Dict[str, Any]]:
        """获取指定位置附近的感官标记"""
        # 使用简单的距离计算，实际项目中可以使用更精确的地理空间索引
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 简单的距离过滤（实际应用中应使用更精确的地理计算）
            lat_range = radius_km / 111.0  # 纬度1度约等于111km
            lon_range = radius_km / (111.0 * abs(lat / 90.0))  # 经度随纬度变化

            cursor.execute("""
                SELECT * FROM sensory_marks
                WHERE latitude BETWEEN ? AND ?
                AND longitude BETWEEN ? AND ?
                ORDER BY created_at DESC
                LIMIT 20
            """, (lat - lat_range, lat + lat_range, lon - lon_range, lon + lon_range))

            marks = []
            for row in cursor.fetchall():
                marks.append({
                    "id": row["id"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "address": row["address"],
                    "quietness": row["quietness"],
                    "smell": row["smell"],
                    "atmosphere": row["atmosphere"],
                    "best_season": row["best_season"],
                    "best_time_of_day": row["best_time_of_day"],
                    "notes": row["notes"],
                    "created_at": row["created_at"]
                })

            return marks

    def add_place(self, place_data: Dict[str, Any]) -> int:
        """添加地点"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO places (
                    latitude, longitude, name, address, place_type
                ) VALUES (?, ?, ?, ?, ?)
            """, (
                place_data.get("latitude"),
                place_data.get("longitude"),
                place_data.get("name"),
                place_data.get("address"),
                place_data.get("place_type")
            ))
            conn.commit()
            return cursor.lastrowid

    def get_place_by_location(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """根据位置获取地点信息"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM places
                WHERE latitude = ? AND longitude = ?
                LIMIT 1
            """, (lat, lon))

            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "name": row["name"],
                    "address": row["address"],
                    "place_type": row["place_type"],
                    "created_at": row["created_at"]
                }
            return None

    def get_places_by_sensory_preferences(
        self, 
        lat: float, 
        lon: float, 
        radius_km: float = 2.0,
        preferences: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """根据感官偏好搜索地点"""
        if preferences is None:
            preferences = {}

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 简单的距离过滤
            lat_range = radius_km / 111.0
            lon_range = radius_km / (111.0 * abs(lat / 90.0))

            # 构建查询条件
            query = """
                SELECT p.*, AVG(m.quietness) as avg_quietness, 
                       GROUP_CONCAT(m.smell) as smells,
                       GROUP_CONCAT(m.atmosphere) as atmospheres
                FROM places p
                LEFT JOIN place_marks pm ON p.id = pm.place_id
                LEFT JOIN sensory_marks m ON pm.mark_id = m.id
                WHERE p.latitude BETWEEN ? AND ?
                AND p.longitude BETWEEN ? AND ?
            """
            params = [lat - lat_range, lat + lat_range, lon - lon_range, lon + lon_range]

            # 添加偏好条件
            if "quietness" in preferences:
                query += " AND m.quietness >= ?"
                params.append(preferences["quietness"])

            if "smell" in preferences:
                query += " AND m.smell LIKE ?"
                params.append(f"%{preferences['smell']}%")

            if "atmosphere" in preferences:
                query += " AND m.atmosphere LIKE ?"
                params.append(f"%{preferences['atmosphere']}%")

            query += " GROUP BY p.id ORDER BY avg_quietness DESC LIMIT 20"

            cursor.execute(query, params)

            places = []
            for row in cursor.fetchall():
                places.append({
                    "id": row["id"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "name": row["name"],
                    "address": row["address"],
                    "place_type": row["place_type"],
                    "avg_quietness": row["avg_quietness"],
                    "smells": row["smells"].split(",") if row["smells"] else [],
                    "atmospheres": row["atmospheres"].split(",") if row["atmospheres"] else [],
                    "created_at": row["created_at"]
                })

            return places

    def get_area_summary(self, bounds: Dict[str, float]) -> Dict[str, Any]:
        """获取指定区域的感官特征摘要"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # 计算区域内的标记点数量
            cursor.execute("""
                SELECT COUNT(*) as count FROM sensory_marks
                WHERE latitude BETWEEN ? AND ?
                AND longitude BETWEEN ? AND ?
            """, (
                bounds.get("min_lat", 0), bounds.get("max_lat", 0),
                bounds.get("min_lon", 0), bounds.get("max_lon", 0)
            ))

            count = cursor.fetchone()["count"]

            if count == 0:
                return {
                    "mark_count": 0,
                    "avg_quietness": None,
                    "common_smells": [],
                    "best_season": "暂无数据",
                    "summary": "此区域暂无用户标记数据"
                }

            # 计算平均安静程度
            cursor.execute("""
                SELECT AVG(quietness) as avg_quietness FROM sensory_marks
                WHERE latitude BETWEEN ? AND ?
                AND longitude BETWEEN ? AND ?
            """, (
                bounds.get("min_lat", 0), bounds.get("max_lat", 0),
                bounds.get("min_lon", 0), bounds.get("max_lon", 0)
            ))

            avg_quietness = cursor.fetchone()["avg_quietness"]

            # 获取常见气味
            cursor.execute("""
                SELECT smell, COUNT(*) as count FROM sensory_marks
                WHERE latitude BETWEEN ? AND ?
                AND longitude BETWEEN ? AND ?
                AND smell IS NOT NULL AND smell != ''
                GROUP BY smell
                ORDER BY count DESC
                LIMIT 5
            """, (
                bounds.get("min_lat", 0), bounds.get("max_lat", 0),
                bounds.get("min_lon", 0), bounds.get("max_lon", 0)
            ))

            common_smells = [row["smell"] for row in cursor.fetchall()]

            # 获取最佳季节
            cursor.execute("""
                SELECT best_season, COUNT(*) as count FROM sensory_marks
                WHERE latitude BETWEEN ? AND ?
                AND longitude BETWEEN ? AND ?
                AND best_season IS NOT NULL AND best_season != ''
                GROUP BY best_season
                ORDER BY count DESC
                LIMIT 1
            """, (
                bounds.get("min_lat", 0), bounds.get("max_lat", 0),
                bounds.get("min_lon", 0), bounds.get("max_lon", 0)
            ))

            best_season_row = cursor.fetchone()
            best_season = best_season_row["best_season"] if best_season_row else "暂无数据"

            # 生成摘要
            quietness_desc = "安静" if avg_quietness >= 4 else "适中" if avg_quietness >= 3 else "喧闹"
            smells_desc = "、".join(common_smells[:3]) if common_smells else "无明显特征"
            summary = f"此区域共有{count}个用户标记点，整体安静程度{avg_quietness:.1f}星({quietness_desc})，常见气味：{smells_desc}，最佳季节：{best_season}"

            return {
                "mark_count": count,
                "avg_quietness": round(avg_quietness, 1) if avg_quietness else None,
                "common_smells": common_smells,
                "best_season": best_season,
                "summary": summary
            }

# 初始化数据库实例
db = DatabaseManager()
