import sys
import webbrowser
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from eda import (
    plot_top10_total_cases,
    plot_top10_total_deaths,
    plot_correlation_heatmap
)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog, QStackedLayout,
    QVBoxLayout, QHBoxLayout, QComboBox, QMessageBox, QCheckBox, QGroupBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap

from preprocessing import load_and_clean_data
from visualization import (
    plot_global_spread_over_time,
    plot_global_cases_deaths,
    plot_continent_cases_deaths,
    plot_lockdowns_vs_cases,
    plot_global_vaccination_progress,
    plot_current_global_snapshot,
    plot_country_trends,
    plot_choropleth_maps_by_continent
)

class CovidDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🦠 COVID-19 Data Visualization Dashboard")
        self.showFullScreen() # Launch the app in fullscreen mode
        self.df = None  # Placeholder for the loaded and preprocessed DataFrame

        # ----------- Set Background Image -----------
        # Applies a blurred background image to the entire dashboard window
        self.setAutoFillBackground(True)
        palette = QPalette()
        background = QPixmap("background.png").scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)

        # ----------- Main Layout Structure -----------
        outer_layout = QVBoxLayout(self)

        # Top-left corner menu toggle button (to show/hide sidebar menu)
        self.toggle_btn = QPushButton("☰ Hide Menu")
        self.toggle_btn.setFixedSize(120, 40)
        self.toggle_btn.setStyleSheet("background-color:rgb(190, 219, 248); color:rgb(25, 82, 138); font-weight: bold;")
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        outer_layout.addWidget(self.toggle_btn, alignment=Qt.AlignLeft)

        # Horizontal layout dividing Sidebar (left) and Main Stack (right)
        self.main_layout = QHBoxLayout()
        outer_layout.addLayout(self.main_layout)

        # ----------- Sidebar Menu -----------
        # Sidebar contains navigation buttons to each section/page
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(int(self.width() * 0.2))
        self.sidebar.setStyleSheet("background-color: rgba(190, 219, 248, 0.8);")
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        # Navigation buttons
        nav_buttons = [
            ("📂 Load CSV File", self.show_load_page),
            ("🛠️ Pre-process Data", self.show_preprocess_page),
            ("📊 EDA Dashboard", self.show_eda_page),
            ("🌍 Global Spread Over Time", self.show_global_spread_page),
            ("📍 Country-Specific Trends", self.show_country_page),
            ("📈 Global Cases & Deaths", self.show_cases_deaths_page),
            ("🗺️ Choropleth Maps (Cases + Deaths)", self.show_choropleth_page),
            ("🧭 Continent-Wise Impact", self.show_continent_impact_page),
            ("🕒 Lockdowns vs Case Surges", self.show_lockdown_page),
            ("💉 Vaccination Progress", self.show_vaccination_page),
            ("📌 Current Snapshot", self.show_snapshot_page),
        ]

        # Dynamically add each button to the sidebar layout
        for label, action in nav_buttons:
            btn = QPushButton(label)
            btn.setFixedHeight(40)
            btn.setStyleSheet("background-color: rgb(25, 82, 138); color: rgb(190, 219, 248); font-size: 14px; font-weight: bold;")
            btn.clicked.connect(action)
            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch() # Push buttons to the top
        self.main_layout.addWidget(self.sidebar)

        # ----------- Main Content Area -----------
        # This QStackedLayout manages switching between different content screens
        self.stack = QStackedLayout()
        self.main_area = QWidget()
        self.main_area.setLayout(self.stack)
        self.main_layout.addWidget(self.main_area, stretch=4)

        # ----------- Register All Pages -----------
        # Each 'create_*_page()' method defines one section of the dashboard
        self.welcome_screen = self.create_welcome_page()
        self.country_page = self.create_country_page()
        self.load_dataset_page = self.create_load_dataset_page()
        self.preprocess_page = self.create_preprocess_page()
        self.eda_page = self.create_eda_page()
        self.global_spread_page = self.create_global_spread_page()
        self.cases_deaths_page = self.create_cases_deaths_page()
        self.choropleth_page = self.create_choropleth_page()
        self.continent_impact_page = self.create_continent_impact_page()
        self.lockdown_page = self.create_lockdown_page()
        self.vaccination_page = self.create_vaccination_page()
        self.snapshot_page = self.create_snapshot_page()

        # Add all pages to the stack so they can be navigated programmatically
        self.stack.addWidget(self.welcome_screen)
        self.stack.addWidget(self.load_dataset_page)
        self.stack.addWidget(self.preprocess_page)
        self.stack.addWidget(self.eda_page)
        self.stack.addWidget(self.global_spread_page)
        self.stack.addWidget(self.country_page)
        self.stack.addWidget(self.cases_deaths_page)
        self.stack.addWidget(self.choropleth_page)
        self.stack.addWidget(self.continent_impact_page)
        self.stack.addWidget(self.lockdown_page)
        self.stack.addWidget(self.vaccination_page)
        self.stack.addWidget(self.snapshot_page)

        self.stack.setCurrentWidget(self.welcome_screen) # Show welcome screen as default on startup

    def toggle_sidebar(self): # This method toggles the visibility of the sidebar menu (left panel with navigation buttons).
        if self.sidebar.isVisible():
            # If sidebar is currently visible, hide it and update the button text
            self.sidebar.hide()
            self.toggle_btn.setText("➤ Show Menu")
        else:
            # If sidebar is hidden, show it and update the button text
            self.sidebar.show()
            self.toggle_btn.setText("☰ Hide Menu")

    '''
    The following methods handle navigation between different sections of the dashboard.
    Each method switches the main content area to the corresponding stacked page (e.g., load page, EDA, visualizations).
    This design allows for clean transitions between different dashboard modules without opening new windows.
    '''

    def show_load_page(self):
        self.stack.setCurrentWidget(self.load_dataset_page)
    
    def show_preprocess_page(self):
        self.stack.setCurrentWidget(self.preprocess_page)

    def show_eda_page(self):
        self.stack.setCurrentWidget(self.eda_page)

    def show_global_spread_page(self):
        self.stack.setCurrentWidget(self.global_spread_page)

    def show_country_page(self):
        self.stack.setCurrentWidget(self.country_page)

    def show_cases_deaths_page(self):
        self.stack.setCurrentWidget(self.cases_deaths_page)
    
    def show_choropleth_page(self):
        if self.df is not None:
            self.stack.setCurrentWidget(self.choropleth_page)
        else:
            QMessageBox.warning(self, "⚠️ Data Missing", "Preprocess the data first.")

    def show_continent_impact_page(self):
        self.stack.setCurrentWidget(self.continent_impact_page)

    def show_lockdown_page(self):
        self.stack.setCurrentWidget(self.lockdown_page)

    def show_vaccination_page(self):
        self.stack.setCurrentWidget(self.vaccination_page)

    def show_snapshot_page(self):
        self.stack.setCurrentWidget(self.snapshot_page)

    '''def back_to_home(self, from_page):
        self.sidebar.show()
        self.stack.setCurrentWidget(self.welcome_screen)'''

    '''
    These methods define the layout and structure of each individual dashboard page.
    Each page is composed of a combination of vertical layouts, informative text boxes,
    interactive buttons or dropdowns, and visual placeholders tailored to the page’s purpose.
    The method returns a QWidget that is added to the main QStackedLayout for seamless navigation.

    '''
    def create_welcome_page(self):
        # Create a blank QWidget to serve as the page container
        page = QWidget()
        layout = QVBoxLayout(page)

        # Create the main title banner
        title = QLabel("The Rise and Fall of COVID-19:\nA Global Journey Through Data")
        title.setFont(QFont("Arial", 34, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; margin-bottom: 10px;")
        title.setFixedHeight(int(self.height() * 0.25))
        layout.addWidget(title)

        # Create a container to hold the welcome text message
        welcome_container = QWidget()
        welcome_container_layout = QVBoxLayout(welcome_container)
        welcome_container_layout.setAlignment(Qt.AlignCenter)

        welcome_box = QLabel("""
            <div style="text-align: center;">
            <p style="font-size: 18px; font-weight: bold; color: #002147; margin-bottom: 10px;">Welcome!</p>
            </div>
        <div style="text-align: justify; font-size: 15px; color: #002147;">
        This dashboard presents a comprehensive, data-driven narrative of the COVID-19 pandemic—one of the most 
        significant global health emergencies of the 21st century. Using reliable data from Our World in Data, 
        it illustrates the progression of the pandemic across countries and continents, offering insight into 
        infection rates, mortality trends, healthcare responses, vaccination campaigns, and the wide-ranging 
        socioeconomic impacts experienced around the world. The visualizations are designed to provide clarity 
        on complex data, helping users trace the timeline of the pandemic and understand its evolving nature from 
        initial outbreak to present day.<br><br>

        The purpose of this project is to foster a deeper understanding of the multifaceted consequences of COVID-19 
        and to support informed decision-making among public health professionals, researchers, and policymakers. 
        By transforming raw data into meaningful visuals, the dashboard empowers users to explore the global and regional effects of the virus with precision and context. It highlights how different parts of the world have responded, adapted, and recovered, shedding light on both challenges and progress throughout the crisis.<br><br>

        Our visualizations are built with interactivity and flexibility in mind. Users can scale graphs, select specific countries or continents, and choose particular years to visualize, enabling a tailored exploration of the data.<br><br>

        We invite you to explore the visualizations and gain perspective on the global journey through the COVID-19 pandemic.<br><br>
        </div>
        """)
        welcome_box.setWordWrap(True)
        welcome_box.setFixedSize(900, 400)
        welcome_box.setAlignment(Qt.AlignTop)
        welcome_box.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); border-radius: 15px; padding: 25px;")

        # Add message box to the center container
        welcome_container_layout.addWidget(welcome_box)
        layout.addWidget(welcome_container)
        
        return page

    def create_load_dataset_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 60% — About Section
        about_container = QWidget()
        about_layout = QVBoxLayout(about_container)
        about_layout.addStretch()
    
        about = QLabel("""<b>About the Dataset</b><br><br>The data presented in this dashboard is sourced from the 
        Our World in Data COVID-19 dataset, a widely trusted and continuously updated repository of global COVID-19 
        statistics. Maintained by the Global Change Data Lab, this dataset compiles information from a wide array of 
        official sources including national governments, public health agencies, the World Health Organization (WHO), 
        and academic institutions like Johns Hopkins University. Its goal is to provide an accurate, accessible, and 
        comprehensive picture of the pandemic’s impact across countries and over time.<br><br>

        This dataset contains daily records for nearly every country in the world, organized in a time series format 
        that captures the evolution of the pandemic. It includes a rich collection of metrics such as total and new 
        confirmed COVID-19 cases and deaths, testing rates, hospitalizations, and vaccination coverage. More advanced 
        indicators such as excess mortality, reproduction rate (R-value), and positivity rate are also included, allowing 
        for deeper analysis and more informed insights.<br><br>

        One of the strengths of the dataset is its standardization of data across countries, using population-adjusted metrics 
        (such as cases or deaths per million people) to facilitate fair comparisons. Each record is linked to a specific country 
        and date, with dozens of associated fields that reflect the state of the pandemic, public health responses, and healthcare 
        capacity. This makes it a versatile and powerful tool for researchers, journalists, policymakers, and developers creating 
        data visualizations or analysis tools.<br><br>

        The dataset is publicly available and open for use under a Creative Commons BY (CC BY 4.0) license, which allows for 
        redistribution and adaptation with appropriate attribution. It can be accessed on GitHub through the official Our World 
        in Data COVID-19 Data repository, where it is updated regularly to reflect the most recent data available from around the world.""")
        about.setWordWrap(True)
        about.setStyleSheet("color: white; font-size: 16px;")
        about.setAlignment(Qt.AlignTop)
    
        about_layout.addWidget(about)
        about_layout.addStretch()
        about_container.setFixedHeight(int(self.height() * 0.6))
        layout.addWidget(about_container)

        # MIDDLE 20% — Buttons with Reduced Width
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        button_container.setFixedHeight(int(self.height() * 0.2))

        # Styling for uniform appearance of all buttons
        button_style = """
            QPushButton {
            font-size: 14px;
            padding: 10px;
            color: rgb(25, 82, 138);
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 8px;
            width: 300px;
            }
        """

        # Button to upload a local CSV file
        upload_btn = QPushButton("📤 Upload CSV File")
        upload_btn.setStyleSheet(button_style)
        upload_btn.clicked.connect(self.load_csv)

        # Button to open OWID GitHub dataset page in browser
        download_btn = QPushButton("🌐 Download Dataset (OWID)")
        download_btn.setStyleSheet(button_style)
        download_btn.clicked.connect(lambda: webbrowser.open("https://github.com/owid/covid-19-data/blob/master/public/data/owid-covid-data.csv"))

        button_layout.addWidget(upload_btn)
        button_layout.addWidget(download_btn)

        layout.addWidget(button_container)

        layout.addStretch()

        return page
    
    def create_preprocess_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 60% — Info section
        info_container = QWidget()
        info_layout = QVBoxLayout(info_container)
        info_layout.addStretch()

        info = QLabel("""<b>Process of Refining the Dataset</b><br><br>
        Preprocessing is a crucial step in any data-driven project, especially when working with real-world datasets 
        like those related to COVID-19. Raw data often contains inconsistencies, missing values, irrelevant information, 
        or formatting issues that can distort analysis and lead to misleading results. Preprocessing ensures that the data 
        is clean, structured, and ready for accurate visualization and interpretation. It allows for reliable comparisons, 
        minimizes errors, and enhances the performance of any subsequent analysis or machine learning tasks.<br><br>

        In this project, we carefully preprocess the COVID-19 dataset from Our World in Data to make it suitable for exploration 
        and visualization. The first step involves parsing the date column into proper datetime format, which is essential for 
        chronological plotting and time series analysis. Next, we filter the dataset to remove aggregate entries like "World" or 
        "Asia", which are not individual countries and can skew country-level analyses. These are identified and excluded by checking 
        the length of the iso_code, retaining only valid three-letter country codes.<br><br>

        We also drop several columns that contain too many missing values or are not directly relevant to the visualizations presented 
        in the dashboard—such as various forms of excess mortality statistics and test unit descriptions. For the remaining numeric columns, 
        we handle missing values by either filling them with zeros or using forward-filling techniques where appropriate, ensuring consistency 
        across data points. Finally, we estimate the number of active COVID-19 cases by subtracting total deaths and total recovered cases 
        (if available) from the total confirmed cases. This derived column provides a useful measure of current caseload trends across countries and over time.<br><br>

        Through this preprocessing pipeline, the data is transformed into a structured and reliable form, ready to power the visual insights displayed throughout the dashboard.<br><br>""")
        info.setWordWrap(True)
        info.setStyleSheet("color: white; font-size: 16px;")
        info.setAlignment(Qt.AlignTop)

        info_layout.addWidget(info)
        info_layout.addStretch()
        info_container.setFixedHeight(int(self.height() * 0.6))
        layout.addWidget(info_container)

        # MIDDLE 20% — Buttons
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        button_container.setFixedHeight(int(self.height() * 0.2))

        # Reusable button style: compact, soft background, consistent width
        button_style = """
            QPushButton {
                font-size: 14px;
                padding: 10px;
                color: rgb(50, 90, 130);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                width: 300px;
            }
        """

        # Button to run data preprocessing
        preprocess_btn = QPushButton("🧮 Preprocess Dataset")
        preprocess_btn.setStyleSheet(button_style)
        preprocess_btn.clicked.connect(self.preprocess_data)

        # Button to view a summary of the cleaned data (row/column count)
        view_btn = QPushButton("👀 View Preprocessed Data")
        view_btn.setStyleSheet(button_style)
        view_btn.clicked.connect(self.view_preprocessed_data)
        
        button_layout.addWidget(preprocess_btn)
        button_layout.addWidget(view_btn)

        layout.addWidget(button_container)

        layout.addStretch()

        return page
    
    def create_eda_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 30% — About the EDA
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.3))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
            <b>About the EDA</b><br><br>
            This Exploratory Data Analysis (EDA) section provides a first look at the structure and quality of the COVID-19 dataset. We begin by examining key attributes such as dataset size, data types, and missing values to ensure reliability and guide data cleaning. These basic checks help us understand what kind of transformations might be needed and which columns are most useful for analysis.<br><br>
            We then dive into targeted visual summaries—highlighting the top 10 countries by total COVID-19 cases and deaths, and presenting a correlation heatmap of key numerical indicators. These visualizations help uncover global hotspots and reveal relationships between metrics like cases, deaths, tests, and vaccinations.<br><br>
        """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)
        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # 10% Spacer
        spacer = QWidget()
        spacer.setFixedHeight(int(self.height() * 0.1))
        layout.addWidget(spacer)

        # EDA Buttons
        button_container = QWidget()
        button_container.setFixedHeight(int(self.height() * 0.3))
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Standardized button appearance for all EDA options
        button_style = """
            QPushButton {
                font-size: 14px;
                color: rgb(25, 82, 138);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 10px;
                width: 300px;
            }
        """

        # Button: Show top 10 countries by total COVID-19 cases
        top_cases_btn = QPushButton("📈 Top 10 Countries by Total Cases")
        top_cases_btn.setStyleSheet(button_style)
        top_cases_btn.clicked.connect(self.show_eda_top_cases)

        # Button: Show top 10 countries by total deaths
        top_deaths_btn = QPushButton("💀 Top 10 Countries by Total Deaths")
        top_deaths_btn.setStyleSheet(button_style)
        top_deaths_btn.clicked.connect(self.show_eda_top_deaths)

        # Button: Display correlation heatmap of key metrics
        corr_btn = QPushButton("📊 Correlation Heatmap")
        corr_btn.setStyleSheet(button_style)
        corr_btn.clicked.connect(self.show_eda_correlation)

        button_layout.addWidget(top_cases_btn)
        button_layout.addWidget(top_deaths_btn)
        button_layout.addWidget(corr_btn)

        layout.addWidget(button_container)

        layout.addStretch()

        return page

    def create_global_spread_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 30% — About Section
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.3))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
            <b>About the Visualization</b><br><br>
            This animated choropleth map provides a global perspective on the progression of COVID-19 over time. Each country is 
            shaded based on the number of confirmed cases reported on a given day, allowing users to observe how the virus spread 
            across borders from early 2020 onward. The timeline slider at the bottom enables users to move through time and examine specific dates.<br><br>
            
            Interactivity Tools: Users can zoom in/out, pan across continents, reset the map, and even save the visualization as an image. 
            Hovering over icons in the top-right corner explains each tool. <br><br>
        """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # 10% Spacer
        spacer = QWidget()
        spacer.setFixedHeight(int(self.height() * 0.1))
        layout.addWidget(spacer)

        # MIDDLE 20% — View Button
        button_container = QWidget()
        button_container.setFixedHeight(int(self.height() * 0.2))
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        view_btn = QPushButton("📊 View Visualization")
        view_btn.setFixedWidth(300)
        view_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: rgb(25, 82, 138);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        view_btn.clicked.connect(self.view_global_spread)

        button_layout.addWidget(view_btn)
        layout.addWidget(button_container)

        # Bottom 40% empty
        layout.addStretch()

        return page

    def create_country_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 40% — About the Visualization
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.4))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
            <b>About the Visualization</b><br><br>
            This line chart focuses on a single country to explore daily new COVID-19 cases, deaths, and vaccination rates using 
            7-day moving averages. This smoothing technique helps filter out daily reporting fluctuations and shows the underlying 
            trends clearly for any country you want. It’s particularly useful to analyze the timing and effectiveness of interventions 
            and public health responses.<br><br>
            
            Interactivity Tools: Toolbar icons allow zooming, panning, scaling the axes, resetting, and exporting the chart as a PNG. Hover on any icon to view its purpose.<br><br>
            """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # 10% Spacer
        spacer = QWidget()
        spacer.setFixedHeight(int(self.height() * 0.1))
        layout.addWidget(spacer)

        # Dropdown and Button
        interaction_container = QWidget()
        interaction_container.setFixedHeight(int(self.height() * 0.3))
        interaction_layout = QVBoxLayout(interaction_container)
        interaction_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.country_dropdown = QComboBox()
        self.country_dropdown.addItem("Select a country...")
        self.country_dropdown.setFixedWidth(300)

        view_btn = QPushButton("📊 Show Country Trends")
        view_btn.setFixedWidth(300)
        view_btn.clicked.connect(self.plot_country_selected)

        button_style = """
            QPushButton {
            font-size: 14px;
            color: rgb(25, 82, 138);
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 8px;
            padding: 10px;
            }
        """

        view_btn.setStyleSheet(button_style)
        self.country_dropdown.setStyleSheet("font-size: 14px; padding: 6px;")

        interaction_layout.addWidget(self.country_dropdown)
        interaction_layout.addWidget(view_btn)
        layout.addWidget(interaction_container)

        layout.addStretch()

        return page

    def create_cases_deaths_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 40% — About section
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.4))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
        <b>About the Visualization</b><br><br>
        This global comparison line chart showcases the total number of COVID-19 cases and deaths over time. It highlights the 
        exponential nature of viral spread, the periodic surges, and plateaus that occurred due to waves and variant-driven spikes. 
        This is valuable for visualizing global health burden and pandemic scale. <br><br>
        
        Interactivity Tools: The plot is equipped with tools for zooming, panning, saving, and resetting, enhancing user interaction and detailed exploration. <br><br>
        """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # 10% spacer
        spacer1 = QWidget()
        spacer1.setFixedHeight(int(self.height() * 0.1))
        layout.addWidget(spacer1)

        # 20% — View Visualization button
        viz_container = QWidget()
        viz_container.setFixedHeight(int(self.height() * 0.2))
        viz_layout = QVBoxLayout(viz_container)
        viz_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        view_btn = QPushButton("📊 View Visualization")
        view_btn.setFixedWidth(300)
        view_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: rgb(25, 82, 138);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 10px;
                }
            """)
        view_btn.clicked.connect(self.view_cases_deaths)

        viz_layout.addWidget(view_btn)
        layout.addWidget(viz_container)

        layout.addStretch()

        return page

    def create_choropleth_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 30% — About the Visualization
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.3))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
            <b>About the Visualization</b><br><br>
            These maps use color shading to illustrate the total number of COVID-19 deaths by country in selected continents 
            and in a specific time period. Darker colors indicate higher death tolls, providing a stark view of the global mortality 
            distribution. Users can interactively switch between metrics (cases, deaths) and explore changes across year ranges and continents. <br><br>
            
            Interactivity Tools: Pan, zoom, reset, and image export options are accessible on the top-right, along with hover-over descriptions for each button.<br><br>
        """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # MIDDLE 50% — Filters and Button
        filter_container = QWidget()
        filter_container.setFixedHeight(int(self.height() * 0.5))
        filter_layout = QVBoxLayout(filter_container)
        filter_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # Continent checkboxes
        self.continent_checkboxes = []
        cont_group = QGroupBox("🌎 Select Continents")
        cont_group.setStyleSheet("QGroupBox { font-size: 26px; font-weight: bold; color: white; }")
        cont_layout = QVBoxLayout()
        for c in ["Africa", "Asia", "Europe", "North America", "South America", "Oceania"]:
            box = QCheckBox(c)
            box.setStyleSheet("font-size: 22px;")
            self.continent_checkboxes.append(box)
            cont_layout.addWidget(box)
        cont_group.setLayout(cont_layout)
        filter_layout.addWidget(cont_group)

        # Year checkboxes
        self.year_checkboxes = []
        year_group = QGroupBox("📅 Select Year Ranges")
        year_group.setStyleSheet("QGroupBox { font-size: 26px; font-weight: bold; color: white; }")
        year_layout = QVBoxLayout()
        for y in ["2020-2021", "2021-2022", "2022-2023", "2023-2024"]:
            box = QCheckBox(y)
            box.setStyleSheet("font-size: 22px;")
            self.year_checkboxes.append(box)
            year_layout.addWidget(box)
        year_group.setLayout(year_layout)
        filter_layout.addWidget(year_group)

        # View button
        view_btn = QPushButton("📊 Show Choropleth Maps")
        view_btn.setFixedWidth(300)
        view_btn.clicked.connect(self.plot_continent_choropleths)
        view_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: rgb(25, 82, 138);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        filter_layout.addWidget(view_btn)
        layout.addWidget(filter_container)

        layout.addStretch()

        return page
    
    def create_continent_impact_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 30% — About section
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.3))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
            <b>About the Visualization</b><br><br>
            This stacked bar chart breaks down total confirmed cases and deaths across six continents. It highlights the disproportionate 
            impact faced by certain regions, especially Asia and Europe, offering insights into continental population, testing capabilities, and healthcare infrastructure.<br><br>
            
            Interactivity Tools: The plot toolbar supports zooming, resetting, panning, and image downloads. Each button's function is visible on hover.<br><br>
        """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # Spacer 10%
        spacer = QWidget()
        spacer.setFixedHeight(int(self.height() * 0.1))
        layout.addWidget(spacer)

        # View Visualization button — 20%
        button_container = QWidget()
        button_container.setFixedHeight(int(self.height() * 0.2))
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        view_btn = QPushButton("📊 View Visualization")
        view_btn.setFixedWidth(300)
        view_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: rgb(25, 82, 138);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        view_btn.clicked.connect(self.view_continent_impact)

        button_layout.addWidget(view_btn)
        layout.addWidget(button_container)

        layout.addStretch()

        return page
    
    def create_lockdown_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 30% — About section
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.3))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
            <b>About the Visualization</b><br><br>
            This dual-axis chart overlays major global lockdown periods with daily case counts. Red bars represent new COVID-19 cases, 
            while the blue line represents the Stringency Index—a composite score reflecting the severity of government policies. The 
            correlation between rising case numbers and lockdowns is evident.<br><br>
            
            Interactivity Tools: Users can interactively explore specific time periods using zoom and pan features, or export the chart for reporting.<br><br>
            """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # 10% Spacer
        spacer = QWidget()
        spacer.setFixedHeight(int(self.height() * 0.1))
        layout.addWidget(spacer)

        # MIDDLE 20% — View Visualization Button
        button_container = QWidget()
        button_container.setFixedHeight(int(self.height() * 0.2))
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        view_btn = QPushButton("📊 View Visualization")
        view_btn.setFixedWidth(300)
        view_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: rgb(25, 82, 138);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        view_btn.clicked.connect(self.view_lockdowns_vs_cases)

        button_layout.addWidget(view_btn)
        layout.addWidget(button_container)

        layout.addStretch()

        return page
    
    def create_vaccination_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 30% — About section
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.3))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
            <b>About the Visualization</b><br><br>
            This line chart shows global vaccination trends, with lines representing at least one dose, full vaccination, 
            and booster administration. Spikes and plateaus indicate phases of vaccine rollout and uptake. It provides an overview of immunization efforts over time.<br><br>
            
            Interactivity Tools: Options include zoom, pan, axis scaling, resetting, and saving. Each toolbar icon reveals its function on hover.<br><br>
        """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # 10% Spacer
        spacer = QWidget()
        spacer.setFixedHeight(int(self.height() * 0.1))
        layout.addWidget(spacer)

        # MIDDLE 20% — View Visualization Button
        button_container = QWidget()
        button_container.setFixedHeight(int(self.height() * 0.2))
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        view_btn = QPushButton("📊 View Visualization")
        view_btn.setFixedWidth(300)
        view_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: rgb(25, 82, 138);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        view_btn.clicked.connect(self.view_vaccination_progress)

        button_layout.addWidget(view_btn)
        layout.addWidget(button_container)

        layout.addStretch()

        return page

    def create_snapshot_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(40, 20, 40, 20)

        # TOP 30% — About the Visualization
        about_container = QWidget()
        about_container.setFixedHeight(int(self.height() * 0.3))
        about_layout = QVBoxLayout(about_container)
        about_layout.setAlignment(Qt.AlignCenter)

        about = QLabel("""
            <b>About the Visualization</b><br><br>
            This real-time choropleth heatmap displays the percentage of population fully vaccinated as of the latest available date. 
            Countries are color-coded to reflect vaccine coverage, helping identify regions that are ahead or lagging in immunization.<br><br>
            
            Interactivity Tools: Zoom, pan, save-as-image, and reset features are present with user-friendly tooltips available upon hover.<br><br>
        """)
        about.setStyleSheet("color: white; font-size: 16px; background-color: rgba(0,0,0,0.4); padding: 15px; border-radius: 12px;")
        about.setWordWrap(True)
        about.setAlignment(Qt.AlignCenter)

        about_layout.addWidget(about)
        layout.addWidget(about_container)

        # 10% Spacer
        spacer = QWidget()
        spacer.setFixedHeight(int(self.height() * 0.1))
        layout.addWidget(spacer)

        # MIDDLE 20% — View Visualization Button
        button_container = QWidget()
        button_container.setFixedHeight(int(self.height() * 0.2))
        button_layout = QVBoxLayout(button_container)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        view_btn = QPushButton("📊 View Visualization")
        view_btn.setFixedWidth(300)
        view_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: rgb(25, 82, 138);
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        view_btn.clicked.connect(self.view_snapshot)

        button_layout.addWidget(view_btn)
        layout.addWidget(button_container)

        layout.addStretch()

        return page

    def load_csv(self): # Load a CSV file through a file dialog and store its path
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.file_path = file_path
            # Notify the user that the file was successfully loaded
            QMessageBox.information(self, "✅ Loaded", f"CSV Loaded:\n{file_path.split('/')[-1]}")

    def preprocess_data(self): # Preprocess the uploaded CSV using custom logic defined in preprocessing.py
        if hasattr(self, 'file_path'):
            # Run data cleaning and transformation logic
            self.df = load_and_clean_data(self.file_path)
            self.update_country_dropdown() # Refresh country dropdown with new data
            QMessageBox.information(self, "✅ Success", "Data preprocessed successfully.")
        else:
            QMessageBox.warning(self, "⚠️ Error", "Please load a file first.")
    
    def view_preprocessed_data(self): # Display a quick summary of the cleaned dataset
        if self.df is not None:
            msg = f"✅ Data has {len(self.df)} rows and {len(self.df.columns)} columns."
            QMessageBox.information(self, "Preprocessed Dataset Info", msg)
        else:
            QMessageBox.warning(self, "⚠️ Not Available", "No data found. Please preprocess first.")

    def update_country_dropdown(self): # Update the country dropdown with valid 3-letter ISO-coded countries
        self.country_dropdown.clear()
        self.country_dropdown.addItem("Select a country...")
        countries = sorted(self.df[self.df['iso_code'].str.len() == 3]['location'].dropna().unique())
        self.country_dropdown.addItems(countries)

    def run_plot(self, func): # Run any visualization function with the preprocessed DataFrame
        if self.df is not None:
            try:
                func(self.df)
            except Exception as e:
                QMessageBox.critical(self, "Plot Error", str(e)) # Show error if plot fails
        else:
            QMessageBox.warning(self, "⚠️ Data Missing", "Preprocess the data first.")

    def plot_country_selected(self): # Trigger country-specific trend visualization based on user selection
        country = self.country_dropdown.currentText()
        if self.df is not None and country != "Select a country...":
            plot_country_trends(self.df, country)
        else:
            QMessageBox.warning(self, "⚠️ No Country Selected", "Choose a country first.")

    def plot_continent_choropleths(self):# 📈 Trigger continent and date specific plot.
        if self.df is None:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please load and preprocess the data.")
            return
        continents = [cb.text() for cb in self.continent_checkboxes if cb.isChecked()]
        years = [cb.text() for cb in self.year_checkboxes if cb.isChecked()]
        if not continents or not years:
            QMessageBox.warning(self, "⚠️ Selection Missing", "Select at least one continent and one year.")
            return
        plot_choropleth_maps_by_continent(self.df, continents, years)

    '''
    These functions handle user-triggered visualizations within the dashboard.
    Each method checks if preprocessed data (self.df) is available before rendering plots.
    Depending on the visualization, relevant plotting functions from external modules are called.
    If data is missing, a warning message box notifies the user to preprocess the dataset first.
    '''
    def show_eda_top_cases(self):
        if self.df is not None:
            from eda import plot_top10_total_cases
            plot_top10_total_cases(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

    def show_eda_top_deaths(self):
        if self.df is not None:
            from eda import plot_top10_total_deaths
            plot_top10_total_deaths(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

    def show_eda_correlation(self):
        if self.df is not None:
            from eda import plot_correlation_heatmap
            plot_correlation_heatmap(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

    def view_global_spread(self):
        if self.df is not None:
            plot_global_spread_over_time(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

    def view_cases_deaths(self):
        if self.df is not None:
            plot_global_cases_deaths(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

    def view_continent_impact(self):
        if self.df is not None:
            plot_continent_cases_deaths(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

    def view_lockdowns_vs_cases(self):
        if self.df is not None:
            plot_lockdowns_vs_cases(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

    def view_vaccination_progress(self):
        if self.df is not None:
            plot_global_vaccination_progress(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

    def view_snapshot(self):
        if self.df is not None:
            plot_current_global_snapshot(self.df)
        else:
            QMessageBox.warning(self, "⚠️ Missing Data", "Please preprocess the dataset first.")

'''
Application Entry Point
This block initializes the Qt application, launches the main dashboard window,
and starts the event loop to keep the GUI responsive. It ensures the code is only
executed when this file is run directly, not when imported as a module.
'''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dashboard = CovidDashboard()
    dashboard.show()
    sys.exit(app.exec_())
  
