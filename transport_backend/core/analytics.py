import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from .models import Booking
from django.db.models.functions import Extract
from datetime import datetime, timedelta
import holidays

def predict_demand(route_id, date_to_predict):
    # 1. Get all bookings for this route
    bookings = Booking.objects.filter(trip__route_id=route_id)
    
    if bookings.count() < 10:
        return 0

    # 2. Process data in Python instead of the Database 
    data_list = []
    for b in bookings:
        data_list.append({
            'day': b.created_at.isoweekday(),
            'hour': b.created_at.hour,
            'seats': b.seat_count
        })
    
    df = pd.DataFrame(data_list)
    
    # 3. Train Model
    X = df[['day', 'hour']]
    y = df['seats']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # 4. Predict
    target_day = date_to_predict.isoweekday()
    target_hour = 8
    
    prediction = model.predict([[target_day, target_hour]])
    final_val = float(prediction[0])

    day_weights = {
        1: 1.2,  # Monday (Busy)
        2: 1.0,  # Tuesday
        3: 1.0,  # Wednesday
        4: 1.1,  # Thursday
        5: 1.3,  # Friday (Travel day)
        6: 0.9,  # Saturday
        7: 0.8   # Sunday (Quiet)
    }

    final_val *= day_weights.get(target_day, 1.0)

    # --- NEW HOLIDAY & SEASON LOGIC STARTS HERE ---
    ng_holidays = holidays.Nigeria()
    
    # A. Check for Public Holidays (Christmas, Eid, etc.)
    if date_to_predict.date() in ng_holidays:
        final_val *= 3.5  # Boost demand by 3.5x
        
    # B. Check for School Rush (Jan 1-15 or Sept 10-25)
    elif (date_to_predict.month == 1 and date_to_predict.day <= 15) or \
         (date_to_predict.month == 9 and 10 <= date_to_predict.day <= 25):
        final_val *= 2.0  # Double the demand
    # --- END OF HOLIDAY LOGIC ---

    return round(final_val, 1)