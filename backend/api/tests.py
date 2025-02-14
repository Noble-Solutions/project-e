from fastapi import APIRouter, Depends
from starlette import status

from core.services.get_service import get_service
from core.services.test_data import TestDataService

router = APIRouter()


@router.post("/create_test_data", status_code=status.HTTP_201_CREATED)
async def create_test_data(
    test_service: TestDataService = Depends(get_service(TestDataService)),
) -> dict:
    test = await test_service.create_test_data()
    return test


@router.post("/delete_test_data", status_code=status.HTTP_200_OK)
async def delete_test_data(
    test_service: TestDataService = Depends(get_service(TestDataService)),
) -> dict:
    test = await test_service.delete_test_data()
    return test
