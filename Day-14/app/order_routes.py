from fastapi import APIRouter, BackgroundTasks

router = APIRouter()


def log_order(order_id: int):
    print(f"Order {order_id} confirmed")


@router.post("/order")
def create_order(background_tasks: BackgroundTasks):
    order_id = 101

    background_tasks.add_task(log_order, order_id)

    return {"message": "Order placed successfully"}
