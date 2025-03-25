import sklearn
import joblib
import pandas as pd
from fastapi import HTTPException
from starlette import status
from service import user_service, order_service


def order_data_by_dummy_columns(old_x_columns , new_data):
    new_data_with_dummy_columns = pd.get_dummies(new_data, drop_first=False)
    missing_dummy_columns = set(old_x_columns) - set(new_data_with_dummy_columns.columns)

    for col in missing_dummy_columns:
        new_data_with_dummy_columns[col] = False

    new_data_with_dummy_columns = new_data_with_dummy_columns[old_x_columns]

    return new_data_with_dummy_columns


async def predict_user_expenses_for_tech_items(user_id: int):
    loaded_model = joblib.load("machine_learning_model/final_customer_model.joblib")
    loaded_polynomial_converter = joblib.load("machine_learning_model/polynomial_converter.joblib")
    loaded_scaler = joblib.load("machine_learning_model/customer_scaler.joblib",  mmap_mode='r')

    user = await user_service.get_by_user_id(user_id)
    user_avg_total_quantity = await order_service.get_avg_total_quantity_for_closed_orders(user.id)

    data = {
        'gender': [user.gender.value],
        'age': [user.age],
        'category': ['Technology'],
        'quantity': [round(user_avg_total_quantity)]
    }

    new_df = pd.DataFrame(data)

    old_x_columns = ['age', 'quantity', 'gender_Male', 'category_Books', 'category_Clothing',
                     'category_Cosmetics', 'category_Food & Beverage', 'category_Shoes',
                     'category_Souvenir', 'category_Technology', 'category_Toys']

    new_data_with_dummy_columns = order_data_by_dummy_columns(old_x_columns, new_df)

    try:
        poly_features = loaded_polynomial_converter.transform(new_data_with_dummy_columns)
        new_scaled_data = loaded_scaler.transform(poly_features)
        prediction = loaded_model.predict(new_scaled_data)
        return prediction

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Prediction error: {str(e)}")
