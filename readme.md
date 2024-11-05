# AI-Powered Bank Marketing Generator

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0-red.svg)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude--2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

An AI-powered solution for generating personalized banking marketing campaigns, ensuring brand compliance while leveraging customer data for targeted messaging across multiple channels.

## 🌟 Key Features

- **AI-Powered Content Generation**
  - Personalized campaign messaging using Claude API
  - Brand-compliant content creation
  - Multi-channel content adaptation

- **Customer Segmentation**
  - Advanced customer profiling
  - Behavior-based segmentation
  - Personalized targeting

- **Multi-Channel Preview**
  - Email campaign previews
  - Mobile app notifications
  - Web content layouts

- **Brand Compliance**
  - Automated guideline adherence
  - Legal disclaimer management
  - Consistent visual elements

- **Performance Analytics**
  - Engagement metrics
  - Channel optimization scores
  - Personalization analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Anthropic API key
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-powered-bank-marketing-generator.git
cd ai-powered-bank-marketing-generator
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run src/main.py
```

2. Access the web interface at `http://localhost:8501`

## 🏗️ Project Structure

```
ai-powered-bank-marketing-generator/
├── src/
│   ├── config/           # Configuration files
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── brand_guidelines.py
│   ├── data/            # Data handling
│   │   ├── __init__.py
│   │   └── synthetic_data.py
│   ├── models/          # Campaign generation
│   │   ├── __init__.py
│   │   ├── campaign_generator.py
│   │   └── customer_insights.py
│   ├── ui/             # User interface
│   │   ├── __init__.py
│   │   ├── components.py
│   │   └── styles.py
│   └── utils/          # Utility functions
│       ├── __init__.py
│       ├── api_utils.py
│       └── cache_utils.py
├── tests/              # Test files
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
└── requirements.txt   # Python dependencies
```

## 🛠️ Configuration

### Environment Variables
Create a `.env` file with the following:
```env
ANTHROPIC_API_KEY=your_api_key_here
DEBUG_MODE=false
ENVIRONMENT=development
```

### Brand Guidelines
Update brand guidelines in `src/config/brand_guidelines.py`:
```python
BRAND_GUIDELINES = {
    'colors': {
        'primary': '#FDB813',  # Update with your brand colors
        'secondary': '#000000'
    },
    # ... other brand settings
}
```

## 🔄 Workflow

1. **Data Generation**
   - Generate synthetic customer data
   - Filter and segment customers

2. **Campaign Creation**
   - Select customer profile
   - Generate personalized campaign
   - Preview across channels

3. **Optimization**
   - Review performance metrics
   - Adjust targeting
   - Export campaign details

## 📊 Features in Detail

### Customer Segmentation
- Premium
- Standard
- Basic

### Channel Support
- Email Campaigns
- Mobile App Notifications
- Web Content
- SMS Messages

### Analytics
- Engagement Rates
- Channel Performance
- Personalization Scores
- Brand Alignment Metrics

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add: some amazing feature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Anthropic Claude API](https://www.anthropic.com/) for AI capabilities
- [Streamlit](https://streamlit.io/) for the web interface
- [Plotly](https://plotly.com/) for data visualization
- [Pandas](https://pandas.pydata.org/) for data handling

## 📧 Contact

Your Name - [@yourgithub](https://github.com/yourgithub)

Project Link: [https://github.com/yourusername/ai-powered-bank-marketing-generator](https://github.com/yourusername/ai-powered-bank-marketing-generator)

## 🚀 Roadmap

- [ ] Add support for more channels
- [ ] Implement A/B testing
- [ ] Add campaign scheduling
- [ ] Enhance analytics dashboard
- [ ] Add custom template support

---
⭐️ Star this repo if you find it helpful!