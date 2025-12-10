import json
from sqlalchemy.orm import Session
from database import Videos, VideoSnapshots, SessionLocal
from datetime import datetime

def json_load():
    with open("videos.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    videos = data["videos"]
    session: Session = SessionLocal()

    try:
        for video in videos:
            v = Videos(
                id=video["id"],
                creator_id=video["creator_id"],
                video_created_at=datetime.fromisoformat(video["video_created_at"]),
                views_count=video.get("views_count"),
                likes_count=video.get("likes_count"),
                comments_count=video.get("comments_count"),
                reports_count=video.get("reports_count"),
            )
            session.add(v)
            session.flush()

            snapshots = video.get("snapshots", [])

            for s in snapshots:
                snap = VideoSnapshots(
                    id = s["id"],
                    video_id = video["id"],
                    views_count=s.get("views_count"),
                    likes_count=s.get("likes_count"),
                    comments_count=s.get("comments_count"),
                    reports_count=s.get("reports_count"),
                    delta_views_count=s.get("delta_views_count"),
                    delta_likes_count=s.get("delta_likes_count"),
                    delta_comments_count=s.get("delta_comments_count"),
                    delta_reports_count=s.get("delta_reports_count"),
                    created_at=datetime.fromisoformat(s["created_at"])
                )
                session.add(snap)

        session.commit()

    except Exception as e:
        session.rollback()

    finally:
        session.close()




if __name__ == "__main__":
    json_load()






