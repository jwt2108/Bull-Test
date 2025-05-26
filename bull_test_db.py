# import background as background
import streamlit as st
import plotly.express as px
import pandas as pd
import datetime as dt
import plotly.graph_objects as go

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1200)

st.set_page_config(layout='wide')

# Read in Data and Massage

df = pd.read_csv('data/TBR_Bull_Tests1-4_2.csv', index_col=0)
df['DOB'] = pd.to_datetime(df['DOB'].astype(str).str.strip(), format='mixed')
df['weigh_in_date'] = pd.to_datetime(df['weigh_in_date'].astype(str).str.strip(), format='mixed')

# Format DOB, Weigh in Date and Test Year to display correctly
df["DOB"] = [
    dt.datetime.strptime(
        str(target_date).split(" ")[0], '%Y-%m-%d').date()
    for target_date in df["DOB"]
]
df["weigh_in_date"] = [
    dt.datetime.strptime(
        str(target_date).split(" ")[0], '%Y-%m-%d').date()
    for target_date in df["weigh_in_date"]
]

df['test_yr'] = df['DOB']
df['test_yr'] = pd.DatetimeIndex(df['test_yr']).year.astype(str)
# df['test_yr'].astype(str)

# print(df.info())
# print(df.info())

# Dashboard Main


test_year = list(df['test_yr'].unique())
print(df['test_yr'].info())

tab1, tab2, tab3, tab4 = st.tabs(
    ['Background Information', 'Bull Test Observations', 'Bull Data Analysis', "Bull Analysis"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        path = './html/background.html'
        with open(path, 'r') as f:
            html_data = f.read()
        st.components.v1.html(html_data, scrolling=True, height=1500)
    with col2:
        st.image('bull_ages.png', caption="Image1: Bulls charted Test Year v Age (Days Old)\n"
                                          "The 'box' plot illustrates the range of age in days "
                                          "for each years bull test")
        st.image('adg_weight_averages.png', caption='Image 2: Average Daily Gain Across All '
                                                    'Years by Weight Check Milestone')

with tab2:
    st.header('Thorbardin Bull Tests')
    st.subheader('Bull tests 1 - 4 conducted 2000 - 2005')

    bull_count_chart = px.histogram(data_frame=df,
                                    x='test_yr',
                                    color='test_yr',
                                    hover_name='test_yr',
                                    title='Bull Entries by Year')
    bull_count_chart.update_xaxes(type='category')
    st.plotly_chart(bull_count_chart)

    # Age Chart
    st.subheader('Test Entry Age Observations')
    st.caption(
        'Bulls entered into these bull tests could generally be considered post weanling bulls. Ages range from ~200 '
        '- ~300 days old. ')
    st.caption('Data is charted by Test Year v Days Old')

    df_sort = df.sort_values(by='test_yr')
    bulls_age_plot = px.box(data_frame=df_sort,
                            y='days_old',
                            x='test_yr',
                            color='test_yr',
                            title='Bulls Starting Age',
                            )
    bulls_age_plot.update_layout(yaxis_title='Starting Ages (Days Old)')

    st.plotly_chart(bulls_age_plot)

    col1, col2 = st.columns(2, gap='small')

    # Weights Start Chart

    with col1:
        st.subheader('Entry Weight Range Observations')
        st.caption('Bulls entered generally were between 400 - 700+ lbs.')
        st.caption('Data is graphed by Test Year v Start Weight')
        bulls_st_wt_plot = px.box(data_frame=df_sort,
                                  y='weigh_in',
                                  x='test_yr',
                                  color='test_yr',
                                  title='Bulls by Starting Weight')
        bulls_st_wt_plot.update_layout(xaxis_title='Measurement Year', yaxis_title='Starting Weights')
        st.plotly_chart(bulls_st_wt_plot)

    # Weights Final Chart
    with col2:
        st.subheader('Final Weight Observations')
        st.caption('Bulls final weights were generally between 600 - 1000+ lbs. '
                   'A coarse observation indicates an average gain between ~200-300 lb. through the test period. Subtracting median'
                   ' entry weight from median final weight for each year to obtain the observable gain. '
                   'The best performance seems to be 2001 with an average gain of 294 lb. ')
        st.caption('Data is graphed by Test Year v Final Weight')
        bulls_fi_wt_plot = px.box(data_frame=df_sort,
                                  y='weight4',
                                  color='test_yr',
                                  title='Bulls by Final Weight')
        bulls_fi_wt_plot.update_layout(yaxis_title='Final Weights')
        st.plotly_chart(bulls_fi_wt_plot)

    # Look at Weight Results over Test Period

    weight_results = ['weigh_in', 'weight1', 'weight2', 'weight3', 'weight4']
    weight_checks = ['weight1', 'weight2', 'weight3', 'weight4']

    adg_results = ['ADG1', 'ADG2', 'ADG3', 'ADG4']

    # Get the mean weight gain between the weight checks
    global list1
    global list2
    list1 = []
    list2 = []
    with col1:

        for check in weight_results:
            mean = df[check].mean().round(2)
            list1.append(mean)

        plot = px.scatter(x=list1,
                          y=weight_results,
                          # markers=True,
                          color=weight_results,
                          size=list1,
                          title='Average Weight for Each Weight Check')
        plot.update_layout(xaxis_title='Average Weight')
        plot.update_layout(yaxis_title='Weight Check')
        st.plotly_chart(plot)

    with col2:

        for adg in adg_results:
            mean = df[adg].mean().round(2)
            list2.append(mean)

        plot = px.scatter(x=list2,
                          y=adg_results,
                          # markers=True,
                          color=adg_results,
                          size=list2,
                          title='Average ADG for Each Weight Check')
        plot.update_layout(xaxis_title='Average ADG')
        plot.update_layout(yaxis_title='Weight Check')
        st.plotly_chart(plot)

    with col1:
        bull_weight_results = px.box(data_frame=df,
                                     y=weight_results,
                                     # color='weight2',
                                     title='Weight Gain Milestones')
        bull_weight_results.update_xaxes(type='category')
        bull_weight_results.update_layout(xaxis_title='Weight Checks')
        bull_weight_results.update_layout(yaxis_title='Weight in lb.')

        st.plotly_chart(bull_weight_results)

    with col2:
        adg_results_plot = px.box(data_frame=df,
                                  y=adg_results,
                                  title='ADG Results')
        adg_results_plot.update_layout(yaxis_title='ADG in lbs')
        adg_results_plot.update_layout(xaxis_title='Weight Checks')
        st.plotly_chart(adg_results_plot)

    # Calculate mean ADG for each weight check
    # Calculate mean Weight Gain for each weight check

    # Build Analysis Scatter Plot

    # MAY BE TOO MANY FIELDS IN THIS CHARTING
    # LOOK AT THINNING DOWN

with tab3:
    col1a, col2a = st.columns(2)
    st.header('Thorbardin Bull Tests')
    cat = ['Bull Name', 'DOB', 'bull_score', 'birth_weight', 'weigh_in_date', 'weigh_in', 'pt_adg', 'est_205d_wt',
           'weight1',
           'ADG1', 'weight2', 'ADG2', 'weight3', 'ADG3', 'weight4', 'ADG4', 'ADG_final', 'ADG_final_ranking', 'WPDA',
           'REA',
           'REA_ranking', 'rea_cwt', 'rea_cwt_ranking', '%IMF', '%IMF_ranking', 'BF', 'scrotal_cm', 'days_old',
           'test_yr']
    cat.sort()


    # Dropdown Menus
    with col1a:
        dropdown_x = st.selectbox(label='Select Category to Chart X Axis',
                                  key='ddx',
                                  options=cat,
                                  help='Select X Category',
                                  )
    with col2a:
        dropdown_y = st.selectbox(label='Select Category to Chart Y Axis',
                                  key='ddy',
                                  options=cat,
                                  help='Select Y Category')

    df_sort_yr = df.sort_values(by='test_yr')
    scatter_plot = px.scatter(data_frame=df_sort_yr,
                              x=dropdown_x,
                              y=dropdown_y,
                              hover_name='Bull Name',
                              color='test_yr',
                              title='Analysis Scatter Plot')

    st.plotly_chart(scatter_plot)

    st.dataframe(df)

with tab4:
    # Get the list of bulls names for selection
    bulls = df['Bull Name']
    bulls = bulls.sort_values().reset_index(drop=True)
    bulls.index += 1

    # Select box for Selected Bull
    dropdown_bull = st.selectbox(label='Select Bull of Interest',
                                 options=bulls,
                                 key='bull_x',
                                 help='Select Bull for Analysis')

    st.write(dropdown_bull)
    sel_bull = df.loc[df['Bull Name'] == dropdown_bull]
    st.write(sel_bull)

    # Show age comparisons

    age_bull = go.Scatter(y=sel_bull['days_old'],
                          x=sel_bull['Bull Name'],
                          mode='markers',
                          marker=dict(size=20),
                          name=dropdown_bull,
                          )
    age_peers = go.Box(y=df['days_old'],
                       name='Peer Age in Days'
                       )

    fig_a = go.Figure()
    fig_a.add_trace(age_bull).update_layout()
    fig_a.add_trace(age_peers).update_layout()
    st.subheader('Age Comparison:\n{} v Peers (Age in Days)'.format(dropdown_bull))
    st.plotly_chart(fig_a)

    # Weight and ADG Data Charts
    show_weight_data = st.checkbox(label="Show Weight / ADG - Results / Comparisons")
    if show_weight_data:
        sel_col1, sel_col2 = st.columns(2, gap='small')

        with sel_col1:
            plot_weight = px.scatter(data_frame=sel_bull,
                                     x='Bull Name',
                                     y=weight_checks,
                                     hover_name='bull_score',
                                     size='value'
                                     ).update_layout(yaxis_title='Weight')
            st.subheader(dropdown_bull)
            st.plotly_chart(plot_weight)
        with sel_col2:
            weight1 = go.Box(
                y=df['weight1'],
                name='Weight Check 1'
            )
            weight2 = go.Box(
                y=df['weight2'],
                name='Weight Check 2'
            )
            weight3 = go.Box(
                y=df['weight3'],
                name='Weight Check 3'
            )
            weight4 = go.Box(
                y=df['weight4'],
                name='Weight Check 4',
            )
            weight_fig = go.Figure()
            weight_fig.add_trace(weight1).update_layout()
            weight_fig.add_trace(weight2).update_layout()
            weight_fig.add_trace(weight3).update_layout()
            weight_fig.add_trace(weight4).update_layout()
            st.subheader('Group Weight Check Results')
            st.plotly_chart(weight_fig)

        adg_col1, adg_col2 = st.columns(2)

        with adg_col1:
            st.subheader(dropdown_bull)
            # Below is needed because some ADG has negative numbers
            # Using px.scatter only will allow integer or float not negative values
            ADG1 = go.Scatter(
                x=sel_bull['Bull Name'],
                y=sel_bull['ADG1'],
                mode='markers',
                marker=dict(size=20),
                name='ADG1')

            ADG2 = go.Scatter(
                x=sel_bull['Bull Name'],
                y=sel_bull['ADG2'],
                mode='markers',
                marker=dict(size=20),
                name='ADG2')

            ADG3 = go.Scatter(
                x=sel_bull['Bull Name'],
                y=sel_bull['ADG3'],
                mode='markers',
                marker=dict(size=20),
                name='ADG3')

            ADG4 = go.Scatter(
                x=sel_bull['Bull Name'],
                y=sel_bull['ADG4'],
                mode='markers',
                marker=dict(size=20),
                name='ADG4'
            )

            fig = go.Figure()
            fig.add_trace(ADG1).update_layout()
            fig.add_trace(ADG2).update_layout()
            fig.add_trace(ADG3).update_layout()
            fig.add_trace(ADG4).update_layout()
            st.plotly_chart(fig)

        with adg_col2:
            st.subheader('Group ADG from Weight Check Results')
            ADG_Box1 = go.Box(
                y=df['ADG1'],
                name='Peers ADG 1'
            )
            ADG_Box2 = go.Box(
                y=df['ADG2'],
                name='Peers ADG 2'
            )

            ADG_Box3 = go.Box(
                y=df['ADG3'],
                name='Peers ADG 3'
            )
            ADG_Box4 = go.Box(
                y=df['ADG4'],
                name='Peers ADG 4'
            )

            fig_2 = go.Figure()
            fig_2.add_trace(ADG_Box1).update_layout()
            fig_2.add_trace(ADG_Box2).update_layout()
            fig_2.add_trace(ADG_Box3).update_layout()
            fig_2.add_trace(ADG_Box4).update_layout()
            st.plotly_chart(fig_2)


    # Show Ultrasound Data and Comparisons
    show_ultrasound = st.checkbox(label='Show Ultrasound Results and Comparisons')
    if show_ultrasound:

        us_col1, us_col2 = st.columns(2)

        with us_col1:
            # IMF Data
            imf_bull = go.Scatter(y=sel_bull['%IMF'],
                                  x=sel_bull['Bull Name'],
                                  name=dropdown_bull,
                                  mode='markers',
                                  marker=dict(size=20)
                                  )
            imf_peers = go.Box(y=df['%IMF'],
                               name='Peer Group %IMF'
                               )
            imf_fig = go.Figure()
            imf_fig.add_trace(imf_bull).update_layout()
            imf_fig.add_trace(imf_peers).update_layout()
            st.subheader(':blue[%IMF] ')
            st.plotly_chart(imf_fig)
        with us_col2:
            # Backfat
            bf_bull = go.Scatter(y=sel_bull['BF'],
                                 x=sel_bull['Bull Name'],
                                 mode='markers',
                                 marker=dict(size=20))
            bf_peer = go.Box(y=df['BF'],
                             name='Peer Group Backfat')
            bf_fig = go.Figure()
            bf_fig.add_trace(bf_bull).update_layout()
            bf_fig.add_trace(bf_peer).update_layout()
            st.subheader(':blue[Backfat]')
            st.plotly_chart(bf_fig)

        rea_col1, rea_col2 = st.columns(2)

        #REA Size
        with rea_col1:
            rea_bull = go.Scatter(y=sel_bull['REA'],
                                  x=sel_bull['Bull Name'],
                                  name=dropdown_bull,
                                  mode='markers',
                                  marker=dict(size=20))
            rea_peers = go.Box(y=df['REA'],
                               name='Peer Group REA Size')

            rea_fig = go.Figure()
            rea_fig.add_trace(rea_bull).update_layout()
            rea_fig.add_trace(rea_peers).update_layout()
            st.subheader(':blue[REA Size]')
            st.plotly_chart(rea_fig)
        with rea_col2:
            # REA Ratio
            ratio_bull = go.Scatter(y=sel_bull['rea_cwt'],
                                    x=sel_bull['Bull Name'],
                                    mode='markers',
                                    marker=dict(size=20)
                                    )
            ratio_peer = go.Box(y=df['rea_cwt'],
                                name='Peer Group REA per 100'
                                )
            ratio_fig = go.Figure()
            ratio_fig.add_trace(ratio_bull).update_layout()
            ratio_fig.add_trace(ratio_peer).update_layout()
            st.subheader(':blue[REA per 100]')
            st.plotly_chart(ratio_fig)



