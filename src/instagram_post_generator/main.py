import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Crew
from tasks import MarketingAnalysisTasks
from agents import MarketingAnalysisAgents

# Load environment variables
load_dotenv()

# Initialize tasks and agents
tasks = MarketingAnalysisTasks()
agents = MarketingAnalysisAgents()

def main():
    st.set_page_config(page_title="Instagram Post Generator",page_icon="📸", layout="wide")
    st.markdown("""
        <h1 style='text-align: center;'>🚀Instagram Post Generator</h1>
        <h4 style='text-align: center; color: gray;'>Get a complete AI-powered marketing strategy for your product</h4>
                <h3 style='text-align: center; color: gray;'>5 minutes to generate a post</h3>
        <hr>
    """, unsafe_allow_html=True)
    
    # User Inputs
    product_website = st.text_input("🌍 Enter the product website:")
    product_details = st.text_area("📝 Additional product details (optional):")
    
    if st.button("Generate Marketing Strategy"): 
        if not product_website:
            st.error("❌ Please enter the product website to proceed.")
            return

        with st.spinner("Generating marketing strategy... This may take a moment."):
            # Create Agents
            product_competitor_agent = agents.product_competitor_agent()
            strategy_planner_agent = agents.strategy_planner_agent()
            creative_agent = agents.creative_content_creator_agent()

            # Create Tasks
            website_analysis = tasks.product_analysis(product_competitor_agent, product_website, product_details)
            market_analysis = tasks.competitor_analysis(product_competitor_agent, product_website, product_details)
            campaign_development = tasks.campaign_development(strategy_planner_agent, product_website, product_details)
            write_copy = tasks.instagram_ad_copy(creative_agent)

            # Crew for Copy
            copy_crew = Crew(
                agents=[product_competitor_agent, strategy_planner_agent, creative_agent],
                tasks=[website_analysis, market_analysis, campaign_development, write_copy],
                verbose=False
            )
            ad_copy = copy_crew.kickoff()

            # Crew for Image
            senior_photographer = agents.senior_photographer_agent()
            chief_creative_diretor = agents.chief_creative_diretor_agent()
            take_photo = tasks.take_photograph_task(senior_photographer, ad_copy, product_website, product_details)
            approve_photo = tasks.review_photo(chief_creative_diretor, product_website, product_details)
            
            image_crew = Crew(
                agents=[senior_photographer, chief_creative_diretor],
                tasks=[take_photo, approve_photo],
                verbose=False
            )
            image = image_crew.kickoff()

        # Display Results
        st.success("✅ Marketing strategy generated successfully!")
        st.subheader("📢 Ad Copy")
        st.markdown(f"""
            <div style='padding: 20px; border-radius: 10px; background-color: #f8f9fa; border: 1px solid #dee2e6;'>
                <p style='font-size: 16px; line-height: 1.6; margin: 0;'>{ad_copy}</p>
        """, unsafe_allow_html=True)
        
        st.subheader("🎨 MidJourney Image Description")
        st.markdown(f"""
                        <div style='padding: 20px; border-radius: 10px; background-color: #f8f9fa; border: 1px solid #dee2e6;'>
                            <p style='font-size: 16px; line-height: 1.6; margin: 0;'>{image}</p>
                    """, unsafe_allow_html=True)
      

if __name__ == "__main__":
    main()