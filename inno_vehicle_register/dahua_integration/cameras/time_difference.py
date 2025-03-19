from datetime import datetime

def time_difference(timestamp1, timestamp2):
    try:
        time_difference = timestamp2 - timestamp1
        print("Time difference:", time_difference)  

        time_diff_sec = time_difference.total_seconds()
        print("Total seconds:", time_diff_sec)

        time_diff_sec_abs = abs(time_diff_sec)
        return time_diff_sec_abs
    except TypeError as e:
        print("Error calculating time difference:", e)
        return None



    
    
        
    

            



