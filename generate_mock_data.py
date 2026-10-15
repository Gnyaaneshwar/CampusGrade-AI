import pandas as pd
import numpy as np
import os

def generate_student_data(num_students=1000):
    np.random.seed(42) # Ensures we get the exact same dataset every time
    
    # Base aptitude acts as a hidden variable to create realistic correlations between features
    aptitude = np.clip(np.random.normal(loc=70, scale=15, size=num_students), 30, 100)
    
    # Generate Features based on aptitude
    attendance = np.clip(aptitude + np.random.normal(0, 10, num_students), 40, 100)
    previous_gpa = np.clip((aptitude / 10) + np.random.normal(0, 0.5, num_students), 3.0, 10.0)
    internal_marks = np.clip(aptitude + np.random.normal(0, 8, num_students), 20, 100)
    
    # Engagement metrics
    assignments_completed = np.clip(np.round((attendance / 100) * 10 + np.random.normal(0, 1, num_students)), 0, 10)
    submission_delay_days = np.clip(np.round((100 - attendance) / 10 + np.random.normal(0, 2, num_students)), 0, 14)
    learning_activity_score = np.clip(aptitude * 0.8 + np.random.normal(0, 10, num_students), 10, 100)
    
    # Calculate a final score to determine the true grade mathematically
    final_score = (
        (internal_marks * 0.4) + 
        (previous_gpa * 10 * 0.2) + 
        (attendance * 0.2) + 
        (learning_activity_score * 0.2)
    ) - (submission_delay_days * 2)
    
    # Map final score to categorical Grade buckets (A, B, C, D, F)
    conditions = [
        (final_score >= 85),
        (final_score >= 70) & (final_score < 85),
        (final_score >= 55) & (final_score < 70),
        (final_score >= 40) & (final_score < 55),
        (final_score < 40)
    ]
    grades = ['A', 'B', 'C', 'D', 'F']
    
    # Compile the final DataFrame
    df = pd.DataFrame({
        'student_id': [f"STU{str(i).zfill(4)}" for i in range(1, num_students + 1)],
        'previous_gpa': np.round(previous_gpa, 2),
        'internal_marks': np.round(internal_marks, 1),
        'attendance_pct': np.round(attendance, 1),
        'assignments_completed': assignments_completed.astype(int),
        'submission_delay_days': submission_delay_days.astype(int),
        'learning_activity_score': np.round(learning_activity_score, 1),
        'final_grade': np.select(conditions, grades, default='F')
    })
    
    return df

if __name__ == "__main__":
    print("Generating synthetic student data...")
    df = generate_student_data(1000)
    
    # Save to the raw data directory
    output_path = "data/raw/synthetic_student_data.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Successfully generated {len(df)} records.")
    print(f"Data saved to: {output_path}")
