import pandas as pd 
import plotly.express as px
import streamlit as st 

st.set_page_config(page_title ="Title",
                   layout= "wide"
)

organization_df = pd.read_excel(
    io='BDAA_Challenge_SHARE_DataExtractV1.xlsx',
    sheet_name = 'organization',
    nrows = 27
)

route_df = pd.read_excel(
    io='BDAA_Challenge_SHARE_DataExtractV1.xlsx',
    sheet_name = 'route',
    nrows = 8111
)

trip_request_df = pd.read_excel(
    io='BDAA_Challenge_SHARE_DataExtractV1.xlsx',
    sheet_name = 'trip_request',
)

vehicle_df = pd.read_excel(
    io='BDAA_Challenge_SHARE_DataExtractV1.xlsx',
    sheet_name = 'vehicle',
)

trip_summary_df =  pd.read_excel(
    io='BDAA_Challenge_SHARE_DataExtractV1.xlsx',
    sheet_name = 'trip_summary',
)
horizontal_space = "<h>"
st.title("The Future of Mobility")

col1, col2, col3 = st.columns(3)

with col1: 
    # aggregated sum of handicapped seats per make 

    handi_per_make = (
        vehicle_df.groupby(by=["make"]).sum()[["handicapped"]].sort_values(by="handicapped")
    )

    handicapped_seats = px.bar(
        handi_per_make,
        x = "handicapped",
        y = handi_per_make.index,
        title = "<b>Total Handicapped Seats by Make</b>",
        template = "plotly_white",
        labels={
                    "handicapped": "Total Handicapped Seats"
        },
    )
        


    st.plotly_chart(handicapped_seats)
    st.markdown(horizontal_space, unsafe_allow_html = True)

with col1:
    #  costs vs estimated miles 
    trip_request_df["true_cost"] = trip_request_df["fare"]-trip_request_df["discount"]


    costs_vs_miles = px.scatter (
        trip_request_df,
        x = "estimated_miles",
        y = "true_cost",
        title = "<b>Costs vs. Estimated Miles Driven</b>",
        template = "plotly_white",
        labels={
                     "estimated_miles": "Estimated Miles Driven",
                     "true_cost": "True Cost (dollars)",
        },
    )
    st.plotly_chart(costs_vs_miles)
    

with col2: 
    # percentage of handicapped seats by year 

    vehicle_df["percent_handicapped"] = (vehicle_df["handicapped"] / vehicle_df["capacity"]) * 100

    percent_handicapped_year = (
        vehicle_df.groupby(by=["year"]).mean()[["percent_handicapped"]].sort_values(by="percent_handicapped")
    )

    handi_per_year= px.bar(
        percent_handicapped_year,
        x = percent_handicapped_year.index,
        y = "percent_handicapped",
        title = "<b>Average Percentage of Handicapped Seats in Cars by Year</b>",
        template = "plotly_white",
        labels={
                     "percent_handicapped": "Average Percentage Of Handicapped Seats",
        },
    )

    st.plotly_chart(handi_per_year)
    st.markdown(horizontal_space, unsafe_allow_html = True)

with col2: 
    # costs by each organization 

    cost_by_organization = (
        trip_request_df.groupby(by=["organization_id"]).mean()[["true_cost"]].sort_values(by="true_cost")
    )

    cost_org = px.bar(
        cost_by_organization,
        x = cost_by_organization.index,
        y = "true_cost",
        title = "<b>Average Trip Costs by Organization</b>",
        template = "plotly_white",
        labels={
                     "true_cost": "Average True Cost (dollars)",
                     "cost_by_organization.index": "Organization Id",
        },
    )

    st.plotly_chart(cost_org)



with col3:
    # speed by handicapped riders count 

    speed_by_handi = px.box(
        trip_summary_df,
        x = "handicapped_riders",
        y = "avg_speed_mph",
        title = "<b>Average Speed vs. Count of Handicapped Riders</b>",

        labels={
                     "handicapped_riders": "Count of Handicapped Riders",
                     "avg_speed_mph": "Average Speed (mph)",
        },
    )

    st.plotly_chart(speed_by_handi)
    st.markdown(horizontal_space, unsafe_allow_html = True)

with col3:
    # pricing mode pie chart 
    organization_counts = (
        organization_df.groupby(['pricing_mode'])['pricing_mode'].count()
    )
    pricing_mode = px.pie(
        organization_counts,
        values = "pricing_mode",
        names = organization_counts.index,
        title = "<b>Pricing Mode Breakdown </b>"
    )


    st.plotly_chart(pricing_mode)
    


