from fastapi import HTTPException, status


def checkUserAuthenticity(user_id: int, current_user_id: int):
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission for this action",
        )
