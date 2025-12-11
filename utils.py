from database import SessionLocal, Videos, VideoSnapshots
from datetime import datetime


def count_videos(session: SessionLocal) -> int:
    return session.query(Videos).count()


def count_videos_by_creator_in_date_range(
        session: SessionLocal,
        creator_id: str,
        start_date: str,
        end_date: str
) -> int:
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)
    return session.query(Videos).filter(
        Videos.creator_id == creator_id,
        Videos.video_created_at.between(start_dt, end_dt)
    ).count()


def count_videos_with_min_views(session: SessionLocal, views: int) -> int:
    return session.query(Videos).filter(Videos.views_count > views).count()


def sum_growth_on_date(session: SessionLocal, date: str) -> int:
    dt = datetime.fromisoformat(date)
    next_day = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = next_day.replace(hour=23, minute=59, second=59)

    total_growth = session.query(
        VideoSnapshots.delta_views_count
    ).filter(
        VideoSnapshots.created_at.between(next_day, end_day)
    ).all()

    return sum([row.delta_views_count for row in total_growth])


def count_videos_with_new_views_on_date(session: SessionLocal, date: str) -> int:
    dt = datetime.fromisoformat(date)
    start_day = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end_day = dt.replace(hour=23, minute=59, second=59, microsecond=999999)

    rows = session.query(VideoSnapshots.video_id).filter(
        VideoSnapshots.created_at.between(start_day, end_day),
        VideoSnapshots.delta_views_count > 0
    ).distinct().all()

    return len(rows)