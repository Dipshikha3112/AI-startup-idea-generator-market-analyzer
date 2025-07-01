from utils.scraper import search_competitors

def analyze_market(interest, region):
    """
    Analyzes the market for a given interest and region, returning scope, revenue potential,
    audience size, competitors, and saturation.
    """
    # Construct search query
    query = f"top {interest} startups in {region} OR {interest} companies in {region}"
    
    # Try scraping competitors
    competitors, count = search_competitors(query)
    
    # Fallback competitor list for EdTech in India, college students
    if not competitors and interest.lower() == "edtech" and "india" in region.lower():
        competitors = [
            "UpGrad",
            "Scaler Academy",
            "Collegedunia",
            "Leverage Edu",
            "Vedantu",
            "Physics Wallah"
        ]
        count = len(competitors)
    
    # Determine market saturation
    saturation = "High" if count > 50 else "Moderate" if count > 10 else "Low"
    
    # Market scope (filtered by interest and region)
    if interest.lower() == "edtech" and "india" in region.lower():
        scope = (
            "The EdTech sector in India, targeting college students, is rapidly growing due to increasing demand for "
            "personalized, accessible learning solutions. With 43.3 million students in higher education (2021-22), "
            "the market is driven by digital adoption, AI integration, and hybrid learning models. The Indian EdTech "
            "market was valued at $163.49 billion in 2024 and is expected to grow at a CAGR of ~20%, reaching $30 "
            "billion by 2031, with potential for further growth in higher education."
        )
    else:
        scope = (
            f"The {interest} sector in {region} is evolving with increasing adoption of technology-driven solutions. "
            "Market growth is driven by digital transformation and demand for scalable, accessible services."
        )
    
    # Estimated revenue potential
    if interest.lower() == "edtech" and "india" in region.lower():
        estimated_revenue = (
            "Potential revenue for a new EdTech startup targeting college students could range from "
            "$1-10 million annually within 3-5 years, depending on scale and monetization (e.g., subscriptions, freemium)."
        )
    else:
        estimated_revenue = (
            f"Potential revenue for a new {interest} startup in {region} varies based on market size and business model, "
            "typically ranging from $500K to $5M annually within 3-5 years."
        )
    
    # Target audience size
    if interest.lower() == "edtech" and "india" in region.lower() and "college students" in region.lower():
        target_audience = (
            "India has ~43.3 million college students (2021-22), with 20.7 million female and 22.6 million male students. "
            "Approximately 60% own smartphones, and 622 million active internet users in 2020 (projected 900 million by 2025) "
            "indicate a large, digitally savvy audience."
        )
    else:
        target_audience = (
            f"The target audience in {region} for {interest} depends on specific demographics and market penetration. "
            "Smartphone and internet adoption are key drivers for digital solutions."
        )
    
    return {
        "scope": scope,
        "estimated_revenue": estimated_revenue,
        "target_audience": target_audience,
        "competitors": competitors,
        "count": count,
        "saturation": saturation
    }