import streamlit as st
import altair as alt
import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
import plotly.graph_objects as px
from mpldatacursor import datacursor
import streamlit.components.v1 as components

import requests
from bs4 import BeautifulSoup




def main():
    
    page = st.sidebar.selectbox("Select Option", [ "Competitor Exploration", "SECI Tenders" , 
     "Latest News" , "New Technologies" , "SWOT Analysis"])
    
    if page == "SECI Tenders":
        #Get Tender Header Data
        dfHdr = pd.read_excel("Tender_Result.xlsx",sheet_name='master')
        dfDtl    = pd.read_excel("Tender_Result.xlsx",sheet_name='details')
        
                
        st.header("SECI Tenders Results")
        st.write("Please select a page on the left.")
        #st.write(dfHdr)
        st.markdown("""
                  <style>
                    table, th, td {
                    border: 1px solid black;
                    }

                    table td {
                        text-align: left;
                    }
                    table th {
                        text-align: left;
                    }
                    table tr {
                        display: table-row;
                        vertical-align: inherit;
                        border-color: inherit;
                    }

                    </style>
                    """, unsafe_allow_html=True)
        str="""
        <table>
        <tr style="background-color:#D5DBDB"><th>Sl No</th><th>Description</th><th>Cap(MW)</th><th>Dated</th><th>NIT Ref No</th></tr>
        """
        for index, row in dfHdr.iterrows():
            str2 =  "% s" % row['TID']
            strCap = "% s" % row['CAP_MW']
            str = str + "<tr style='background-color:#F2F3F4'><td>" + str2 +"</td><td>" + row['Tender_Description']+ "</td><td>" + strCap + "</td><td>" +  row['DATED']+ "</td><td>" +  row['NIT_REF_NO']+ "</td></tr>"
            str = str + "<tr><td colspan='5'>" 
            str = str + """
            <table>
            <tr style='background-color:#82E0AA'><th>Bidder</th><th>Bid Cap(MW)</th><th>Tariff(Rs/kWh)</th><th>Awarded Cap(MW)</th></tr>
            """
            for index, row2 in dfDtl.iterrows():
                str2 =  row2['TID']

                if str2==row['TID']:
                    strCapBid = "% s" % row2['CAP_MW']
                    strTariff = "% s" % row2['TARIFF_INR_KW']
                    strCapAwrd = "% s" % row2['AWARDED_CAP_MW']
                    str = str + "<tr style='background-color:#EAFAF1'><td>" + row2['Bidder_Name'] +"</td><td>" + strCapBid + "</td><td>" + strTariff + "</td><td>" + strCapAwrd  + "</td></tr>"

            str = str + "</td></tr>" 
            str = str + " </table> "
            
        str = str + "</table>"
        st.markdown(str, unsafe_allow_html=True)


        #st.table(dfHdr)

    elif page == "Competitor Exploration":
        st.title("Comparison on Various Parameters")
        df = pd.read_excel("Comparison2.xlsx",index_col=None)
        dfCap = df[['company_name','CAPACITY', 'COAL_CAPACITY']]

        #Stacked Bar Chart
        labels = df['company_name']
        coal_cap = df['COAL_CAPACITY']
        re_cap = df['Renewal_Commissioned']
        width = 0.35       # the width of the bars: can also be len(x) sequence

        fig, ax = plt.subplots()

        ax.bar(labels, coal_cap, width,  label='Coal Capacity')
        ax.bar(labels, re_cap, width,  bottom=coal_cap, label='Renewable Capacity')

        ax.set_ylabel('Capacity in GW')
        ax.set_title('Generation Portfolio')
        ax.legend()
        
        st.write(fig)


        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)


        #Total Capacity Pie Chart
        st.header("Installed Capacity(total) in GW")
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')        
        explode = (0.2,0.1, 0.1, 0.1,   0.1)
        data = df['CAPACITY']
        lbls = df['company_name']
        total = sum(data)
        ax.pie(data, explode=explode, labels = lbls,
                autopct=lambda p: '{:.0f}'.format(p * total / 100), 
                shadow = True,)
        st.write(fig)


        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)



        #Renewable commissioned Pie Chart
        st.header("Installed Green Capacity in GW")
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')        
        explode = (0.2,0.1, 0.1, 0.1,   0.1)
        data = df['Renewal_Commissioned']
        lbls = df['company_name']
        total = sum(data)
        ax.pie(data, explode=explode, labels = lbls,
                autopct=lambda p: '{:.0f}'.format(p * total / 100), 
                shadow = True,)
        st.write(fig)
        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)



        #Renewable commissioned by 2023 Pie Chart
        st.header("Green Capacity in pipeline (commissioned by 2023) in GW")
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')        
        explode = (0.2,0.1, 0.1, 0.1,   0.1)
        data = df['REN_CAP_BY_2023']
        lbls = df['company_name']
        total = sum(data)
        ax.pie(data, explode=explode, labels = lbls,
                autopct=lambda p: '{:.0f}'.format(p * total / 100), 
                shadow = True,)
        st.write(fig)
        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)


        #Revenue Pie Chart
        st.header("Revenue Comparison")
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        langs = ['C', 'C++', 'Java', 'Python', 'PHP']
        students = [23,17,35,29,12]
        explode = (0.2,0.1, 0.1, 0.1,   0.1)
        ax.pie(df['Revenue'], explode=explode, labels = df['company_name'],
                autopct=lambda pct: func(pct, df['Revenue']), 
                shadow = True,)
        st.write(fig)
        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)



        #EBIDTA Pie Chart
        st.header("EBITDA Comparison")
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')        
        explode = (0.2,0.1, 0.1, 0.1,   0.1)
        data = df['EBITDA']
        lbls = df['company_name']
        ax.pie(data, explode=explode, labels = lbls,
                autopct=lambda pct: func(pct, data), 
                shadow = True,)
        st.write(fig)

        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)


        #combined pie chart
        st.subheader("Revenue and EBITDA Graph")

        dfTmp = df[['company_name','Revenue', 'EBITDA']]
        if st.checkbox('Show data',key='RevEbitda'):           
            st.table(dfTmp.assign(hack='').set_index('hack'))
        
        fig = plt.figure()

        explode = (0.0,0.0, 0.0, 0.0,   0.0)
        data = df['Revenue']
        lbls = df['company_name']
        
        ax1 = fig.add_axes([0, 0, .5, .5], aspect=1)
        ax1.pie(data, explode=explode, labels = lbls,
                autopct=lambda pct: func(pct, data), 
                shadow = True, radius = 1.2)

        explode = (0.0,0.0, 0.0, 0.0,   0.0)
        data = df['EBITDA']
        lbls = df['company_name']
        
        ax2 = fig.add_axes([.5, .0, .5, .5], aspect=1)
        ax2.pie(data, explode=explode, labels = lbls,
                autopct=lambda pct: func(pct, data), 
                shadow = True, radius = 1.2)
        ax1.set_title('Revenue\n\n')
        ax2.set_title('EBITDA\n\n')      
        st.write(fig)
        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        st.subheader("Total Installed Capacity Data")
        dfCap = df[['company_name','CAPACITY']]
        if st.checkbox('Show data', key='Cap'):           
            st.table(dfCap.assign(hack='').set_index('hack'))
 
                
        graph = alt.Chart(dfCap).mark_bar().encode(
            x=alt.X('company_name',  title = 'Company Name') ,         
            y=alt.Y('CAPACITY', title='Capacity in GW'),
            tooltip=[alt.Tooltip('company_name', title='Company'), alt.Tooltip('CAPACITY', title='Coal Capacity')]
        ).properties(
                            width=700,
                            height=550
                        )
        st.write(graph)

        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)



        dfCap = df[['company_name','COAL_CAPACITY']]
        st.subheader("Coal Mining Capacity Data")        
        graph = alt.Chart(dfCap).mark_bar().encode(
            x=alt.X('company_name',  title = 'Company Name') ,         
            y=alt.Y('COAL_CAPACITY', title='Capacity in GW'),
            tooltip=[alt.Tooltip('company_name', title='Company'), alt.Tooltip('COAL_CAPACITY', title='Coal Capacity')]
        ).properties(
                            width=700,
                            height=550
                        )
        st.write(graph)
        st.markdown("<hr style='border-top: 1px dashed green;'/>", unsafe_allow_html=True)


    elif page == "Latest News":
        st.header("Latest News...")

        option = st.selectbox(
            'Select option to get announcements',
            ('IEA', 'Ministry of Power', 'SolarPowerWorldOnline.com'))
        st.write('You selected:', option)

        if option =='IEA':
            lr = getIEANew()
            df = pd.DataFrame(lr, columns = ['Description', 'Type' , 'Link'])
        elif option =='Ministry of Power':
            df = getMoPNews()
        elif option=='SolarPowerWorldOnline.com':
            df = getSPWNews()


        st.markdown("""
                  <style>
                    table, th, td {
                    border: 1px solid black;
                    }

                    table td {
                        text-align: left;
                    }
                    table th {
                        text-align: left;
                    }
                    table tr {
                        display: table-row;
                        vertical-align: inherit;
                        border-color: inherit;
                    }

                    </style>
                    """, unsafe_allow_html=True)
        str="""
        <table>
        <tr style="background-color:#D5DBDB"><th>Sl No</th><th>Description</th><th>News Type</th><th>Web Link</th></tr>
        """
        for index, row in df.iterrows():
            if index>19:
                continue
            str2 =  "% s" % (index+1)
            str = str + "<tr style='background-color:#F2F3F4'><td>" + str2 +"</td><td>" + row['Description']+ "</td><td>" + row['Type'] + "</td><td>" +  row['Link']+ "</td></tr>"

        str = str + "</table>"
        st.markdown(str, unsafe_allow_html=True)

    elif page == "New Technologies":
        
        st.header("New Technologies Worldwide")
        

        # bootstrap 4 collapse example
        components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div id="accordion">
        <div class="card">
            <div class="card-header" id="headingOne">
            
                <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                <h2 style='text-align: left; color: #008080;'>Battery storage and power utility</h2>
                </button>
           
            </div>
            <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
            <div class="card-body">
                <p>Ongoing research in storage technology has resulted in reduced cost of lithium-ion (Li-ion) batteries and an increase in their performance.</p>
    <p>            
    With this trend to continue, utilities in future are expected to switch to large battery banks as an alternative to building new power plants.
    </p><p>
    The advantages are manifold.
    </p>
    <p>
    Firstly, battery storage can be effectively used to tackle peak demand. It is a known fact that demand varies not only on a daily basis but also seasonally and annually. Meeting the peak demand is a costly affair, as utilities have to either invest in additional capacity by building new power plants, which are not always optimally run, or buy power from independent power producers (IPP) during peak hours at higher prices compared to non-peak hours
    </p>
    
    <p>
    On the other hand, grid-connected battery storage can effectively inject the required power into the grid at the right time to meet the demand. Power from battery storage will not only save the utilities from the above-mentioned challenges but also help in maintaining grid balance.</p>
    
    
            </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header" id="headingTwo">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                <h2 style='text-align: center; color: #008080;'>Microbial Fuel Cell (MFC) technology</h2>
                </button>
            </h5>
            </div>
            <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordion">
            <div class="card-body">
                A microbial fuel cell (MFC) is a bio-electrochemical system that drives an electric current by using bacteria and a high-energy oxidant such as O2, mimicking bacterial interactions found in nature. MFCs can be grouped into two general categories: mediated and unmediated. The first MFCs, demonstrated in the early 20th century, used a mediator: a chemical that transfers electrons from the bacteria in the cell to the anode. Unmediated MFCs emerged in the 1970s; in this type of MFC the bacteria typically have electrochemically active redox proteins such as cytochromes on their outer membrane that can transfer electrons directly to the anode. In the 21st century MFCs have started to find commercial use in wastewater treatment.
            </div>
            </div>
        </div>

        <div class="card">
            <div class="card-header" id="headingThree">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                <h2 style='text-align: center; color: #008080;'>Green Hydrogen</h2>
                </button>
            </h5>
            </div>
            <div id="collapseThree" class="collapse" aria-labelledby="headingThree" data-parent="#accordion">
            <div class="card-body">
                Green hydrogen is produced using renewable energy and electrolysis to split water and is distinct from grey hydrogen, which is produced from methane and releases greenhouse gases into the atmosphere, and blue hydrogen, which captures those emissions and stores them underground to prevent them causing climate change
            </div>
            </div>
        </div>


        <div class="card">
            <div class="card-header" id="headingFour">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseFour" aria-expanded="false" aria-controls="collapseFour">
                <h2 style='text-align: center; color: #008080;'>Nuclear Fusion Power</h2>
                </button>
            </h5>
            </div>
            <div id="collapseFour" class="collapse" aria-labelledby="headingFour" data-parent="#accordion">
            <div class="card-body">
                Fusion power offers the prospect of an almost inexhaustible source of energy for future generations, but it also presents so far insurmountable engineering challenges. The fundamental challenge is to achieve a rate of heat emitted by a fusion plasma that exceeds the rate of energy injected into the plasma. Fusion energy would eliminate the need for fossil fuels and solve the intermittency and reliability concerns inherent with renewable energy sources. The energy would be generated without the dangerous amounts of radiation that raises concerns about fission nuclear energy. “First plasma” in ITER (the start of preliminary D-D operation) is currently scheduled to begin in 2025, but the start of full power D-T operation (the reaction between deuterium and tritium), which will allow an attempt at achieving breakeven conditions, has been pushed back almost two decades from the original start date and will now begin in 2035
            </div>
            </div>
        </div>



        <div class="card">
            <div class="card-header" id="headingFive">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapseFive" aria-expanded="false" aria-controls="collapseFive">
                <h2 style='text-align: center; color: #008080;'>Tidal Power</h2>
                </button>
            </h5>
            </div>
            <div id="collapseFive" class="collapse" aria-labelledby="headingFive" data-parent="#accordion">
            <div class="card-body">
                <p>Tidal power or tidal energy is harnessed by converting energy from tides into useful forms of power, mainly electricity using various methods.</p> <p>Although not yet widely used, tidal energy has the potential for future electricity generation. Tides are more predictable than the wind and the sun. Among sources of renewable energy, tidal energy has traditionally suffered from relatively high cost and limited availability of sites with sufficiently high tidal ranges or flow velocities, thus constricting its total availability. However, many recent technological developments and improvements, both in design (e.g. dynamic tidal power, tidal lagoons) and turbine technology (e.g. new axial turbines, cross flow turbines), indicate that the total availability of tidal power may be much higher than previously assumed and that economic and environmental costs may be brought down to competitive levels.</p>
            </div>
            </div>
        </div>

        </div>
        """,
        height=1000
    )

    elif page == "SWOT Analysis":
        st.title("NTPC Ltd.")
        components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        
  
        <div class='row'>
            <div class="card text-white bg-success mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Strength</div>
            <div class="card-body">    
                <p class="card-text">
                    <ul>
                        <li>Employee friendly work culture policies</li>
                        <li>Efficient production process of plants</li>
                        <li>Fully integrated project management system</li>
                        <li>Decades of experience in the sector </li>
                        <li>Backing of Central Government</li>
                        <li>Efficient & timely completion of projects</li>
                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;

            <div class="card text-white bg-warning mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Opportunity</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Huge demand and supply gap</li>
                        <li>Large opportunity in energy consultancy service</li>
                        <li>New sources of power generations</li>
                    </ul>
                </p>
            </div>
            </div>

        </div>

        <div class='row'>
            <div class="card text-white bg-info mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Weakness</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Depleting input materials sources</li>
                        <li>Govt intervention can often cause disruptions in operations</li>
                        <li>Prices are determined by India's Electricity Act</li>
                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;
            <div class="card text-white bg-danger mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Risks</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Rising cost of production</li>
                        <li>Huge competition from growing private sector firms</li>
                        <li>New and cleaner  sources of power</li>
                    </ul>
                </p>
            </div>
            </div>
        </div>
         """,
        height=600
    )


        st.title("Adani")
        components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        
  
        <div class='row'>
            <div class="card text-white bg-success mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Strength</div>
            <div class="card-body">    
                <p class="card-text">
                    <ul>
                        <li>The diversified nature of the Adani Group helps in the growth of Adani Power</li>
                        <li> A strong Project - Execution record</li>
                        <li> Operating Profit to Sales ratio for Adani Power is higher than the National average</li>
                        <li> Since the largest supplier of coal is Adani Enterprises, this reduces the cost of coal to Adani Power</li>
                        <li>One of the major players in the Indian power industry</li>
                        <li>Has a small yet effective workforce of approx 2000 employees</li>

                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;

            <div class="card text-white bg-warning mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Opportunity</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Can diversify into Hydro-electric power generation</li>
                        <li>Adani Group has a presence in coal imports and coal mining. This offers a significant opportunity for Adani Power to expand its operations and compete with other contenders for UMPPs</li>
                        <li>Opportunity to establish presence in other parts of the country</li>

                    </ul>
                </p>
            </div>
            </div>

        </div>

        <div class='row'>
            <div class="card text-white bg-info mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Weakness</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Present only in very few states namely Gujarat, Maharashtra and Haryana</li>
                        <li>Has a very low market share even compared to the private players like Tata Power and Reliance Power</li>

                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;
            <div class="card text-white bg-danger mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Risks</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Changes in International prices of coal</li>
                        <li>Changes in International policies regarding import of coal</li>
                        <li>Increase in private sector power generation could lead to compressed rates of merchant power</li>

                    </ul>
                </p>
            </div>
            </div>
        </div>
         """,
        height=800
    )

        st.title("ENEL")
        components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        
  
        <div class='row'>
            <div class="card text-white bg-success mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Strength</div>
            <div class="card-body">    
                <p class="card-text">
                    <ul>
                        <li>A very large and diverse portfolio generating power from various sources – Gas, Hydel, Coal, Nuclear, Geothermal, and Wind and has vertically integrated operations</li>
                        <li> Present in 40 countries spanning across 4 continents, having 75000 Employees worldwide </li>
                        <li> Very large power generation capacity and very sound financial capacity</li>
                        <li> Has focused on carbon free energy </li>
                        <li>Has a strong employee force of nearly 80,000</li>
                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;

            <div class="card text-white bg-warning mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Opportunity</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>For a company of its size, it has ample scope in India, Africa, the Middle east etc</li>
                        <li> Growing demand for power</li> 
                        <li> Govts supporting cleaner means of power</li>
                    </ul>
                </p>
            </div>
            </div>

        </div>

        <div class='row'>
            <div class="card text-white bg-info mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Weakness</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Focussed mainly in Europe –very less presence in Asia and very less presence in Africa</li>
                        <li>Allegedly Involved in few legal proceedings</li>
                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;
            <div class="card text-white bg-danger mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Risks</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Increase in prices of Gas</li>
                        <li>Varying government policies in other countries (outside Europe) </li>
                        <li>Eurozone crisis</li>

                    </ul>
                </p>
            </div>
            </div>
        </div>
         """,
        height=700
    )

        st.title("ENGIE")
        components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        
  
        <div class='row'>
            <div class="card text-white bg-success mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Strength</div>
            <div class="card-body">    
                <p class="card-text">
                    <ul>
                        <li>Efficient Process and IT communication systems</li>
                        <li>High R&D investments especially in environmental innovations</li>
                        <li>UK’s largest generator and distributor of electricity</li>
                        <li>High ROE & Growth shows its financial growth</li>
                        <li>The organization has over 13,000+ employees</li>
                        <li>Approx 6 million customers are present with the company</li>

                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;

            <div class="card text-white bg-warning mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Opportunity</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Stress on clean Nuclear energy is increasing</li>
                        <li>Can tap other markets for more business</li>
                        <li>Can do upward integration – Electric devices as a package</li>

                    </ul>
                </p>
            </div>
            </div>

        </div>

        <div class='row'>
            <div class="card text-white bg-info mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Weakness</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Presence only in UK means geographic limitation</li>
                        <li> Gas division is yet to mature – Low ROE compared to global leaders</li>
                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;
            <div class="card text-white bg-danger mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Risks</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Volatility in commodity prices</li>
                        <li> High Competition means reduction in market share</li>
                        <li> Regulations on Environment</li>
                    </ul>
                </p>
            </div>
            </div>
        </div>
         """,
        height=650
    )

        st.title("EDF")
        components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        
  
        <div class='row'>
            <div class="card text-white bg-success mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Strength</div>
            <div class="card-body">    
                <p class="card-text">
                    <ul>
                        <li>Efficient Process and IT communication systems</li>
                        <li>High R&D investments especially in environmental innovations</li>
                        <li>UK’s largest generator and distributor of electricity</li>
                        <li>High ROE & Growth shows its financial growth</li>
                        <li>The organization has over 13,000+ employees</li>
                        <li>Approx 6 million customers are present with the company</li>

                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;

            <div class="card text-white bg-warning mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Opportunity</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Stress on clean Nuclear energy is increasing</li>
                        <li>Can tap other markets for more business</li>
                        <li>Can do upward integration – Electric devices as a package</li>

                    </ul>
                </p>
            </div>
            </div>

        </div>

        <div class='row'>
            <div class="card text-white bg-info mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Weakness</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Presence only in UK means geographic limitation</li>
                        <li> Gas division is yet to mature – Low ROE compared to global leaders</li>
                    </ul>
                </p>
            </div>
            </div>

            &nbsp;&nbsp;&nbsp;
            <div class="card text-white bg-danger mb-2" style="max-width: 22rem;">
            <div class="card-header" style="font-weight:bold; font-style:italic;">Risks</div>
            <div class="card-body">
                <p class="card-text">
                    <ul>
                        <li>Volatility in commodity prices</li>
                        <li> High Competition means reduction in market share</li>
                        <li> Regulations on Environment</li>
                    </ul>
                </p>
            </div>
            </div>
        </div>
         """,
        height=650
    )


def load_data_tender():
    df = pd.read_excel("Tender_Result.xlsx")
    return df



def load_data_cap():
    df = pd.read_excel("Comparison.xlsx")
    return df[0:1]

def load_data_cap2():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','CAPACITY']]



def load_coal_cap():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','COAL_CAPACITY']]


def load_rep2023_cap():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','REN_CAP_BY_2023']]


def load_coal_commissioned_cap():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Coal_Commissioned']]


def load_re_commissioned_cap():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Renewal_Commissioned']]


def load_coal_under_cap():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Coal_Under_construction']]


def load_re_under_cap():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Renewal_under_construction']]


def load_revenue():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Revenue']]


def load_EBITDA():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','EBITDA']]


def load_cash_ratio():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Cash_Ratio']]


def load_current_ratio():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Current_Ratio']]


def load_quick_ratio():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Quick_Ratio']]


def load_total_asset():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Total_Asset']]


def load_total_liability():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Total_Liability']]


def load_liability_asset_ratio():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Total_Liabilities_Total Assets_Perc']]


def load_logn_term_debt():
    df = pd.read_excel("Comparison2.xlsx",index_col=None)
    return df[['company_name','Long-Term_Debt']]


def visualize_data(df, x_axis, y_axis):
    graph = alt.Chart(df).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        color='Origin',
        tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    ).interactive()

    st.write(graph)


def getIEANew():
    url = 'https://www.iea.org/news'
    page = requests.get(url)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())
    lr = list()
    
    news = soup.find_all(class_='m-news-listing')
    #print(news)
    for i, val in enumerate(news):
        #print(i,'->',val.text)
        listNews = list()
        lll = val.text.splitlines()       

        for val2 in lll:
            ttt = val2.strip()
            if(len(ttt)>0):
                listNews.append(val2.strip())
        
        links = val.findAll('a')
        for a in links:
            #print('https://www.iea.org'+a['href'])
            listNews.append("<a href='https://www.iea.org"+a['href']+"' target='_blank'>More details</a>")
        #print(lr) 
        lr.append(listNews)
    return lr


#Get Power Ministry News
def getMoPNews():
    url = 'https://powermin.gov.in/en/announcements'
    page = requests.get(url, verify=False)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())

    listDates = list()
    news = soup.find_all(class_='date')
    for i, val in enumerate(news):
        #print(i,'->',val.text)
        listDates.append(val.text)

    listNews = list()
    listLinks = list()
    news = soup.find_all(class_='col-md-10')
    for i, val in enumerate(news):
        #print(i,'->',val.text)
        listNews.append(val.text)
        links = val.findAll('a')
        for a in links:
            #print('https://www.iea.org'+a['href'])
            listLinks.append("<a href='"+a['href']+"' target='_blank'>More details</a>")

    df = pd.DataFrame(list(zip(listNews, listDates, listLinks)),
               columns = ['Description', 'Type' , 'Link'])
    return df


def getSPWNews():
    url = 'https://www.solarpowerworldonline.com/category/industry-news'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    print(page, page.status_code)

    soup = BeautifulSoup(page.text, 'html.parser')
    #print(soup.prettify())

    listDates = list()
    news = soup.find_all(class_='entry-meta')
    for i, val in enumerate(news):
        #print(i,'->',val.text)
        listDates.append(val.text)

    listNews = list()
    listLinks = list()
    news2 = soup.find_all(class_='entry-title')
    for i, val in enumerate(news2):
        print(i,'->',val.text)
        listNews.append(val.text)
        links = val.findAll('a')
        for a in links:            
            listLinks.append("<a href='"+a['href']+"' target='_blank'>More details</a>")


    #print(listLinks)

    df = pd.DataFrame(list(zip(listNews, listDates, listLinks)),
               columns = ['Description', 'Type' , 'Link'])
    return df


# Creating autocpt arguments
def func(pct, allvalues):
    absolute = int(pct / 100.*np.sum(allvalues))
    return "{:.1f}%\n(Rs. {:d} )".format(pct, absolute)

if __name__ == "__main__":
    main()
    #lr = getIEANew()
    #print(lr)
    #df = pd.DataFrame(lr, columns = ['Description', 'Type' , 'Link'])
    #print(df)