# YouTubeChannelPerformance-Dashboard

This is a Streamlit-based interactive web application that provides detailed insights into YouTube channel performance metrics such as views, watch hours, likes, comments, and subscribers. The dashboard supports filtering by date, aggregation over time frames, and visualization with customizable charts.


## Features

1. **Interactive Date Filtering**  
   - Select a custom date range for analysis.  

2. **Time Aggregation Options**  
   - View data aggregated as **Daily, Weekly, Monthly, or Quarterly**.  

3. **Top Performing Insights**  
   - Identify top-performing days or periods for key metrics:  
     - Views  
     - Watch Hours  
     - Net Subscribers  
     - Likes  

4. **Customizable Visualizations**  
   - Choose between **Bar** or **Area** charts to display performance trends.  

5. **Growth Insights**  
   - Line charts to visualize growth trends for selected time frames.  

6. **Download Filtered Data**  
   - Export the filtered dataset as a CSV file for further analysis.  

7. **Raw Data View**  
   - Expand to view the complete dataset after applying filters.  


## How to Run the App

### **Prerequisites**  
Ensure the following are installed:  
- Python 3.x  
- Required Python libraries:  
  ```bash
  pip install streamlit pandas
  ```

### **Run the Streamlit App** 

Run the Streamlit app:  
   ```bash
   streamlit run dashboard.py
   ```
   
## **Data File**  
The application uses `data.csv` containing the following columns:  
- **DATE**: Date of metrics recorded  
- **VIEWS**: Total views on that date  
- **WATCH_HOURS**: Total watch hours accumulated  
- **SUBSCRIBERS_GAINED**: Subscribers gained  
- **SUBSCRIBERS_LOST**: Subscribers lost  
- **LIKES**: Total likes received  
- **COMMENTS**: Total comments received  
- **SHARES**: Total shares recorded  


## Output


