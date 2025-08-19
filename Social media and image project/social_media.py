import openai
from pathlib import Path
import requests

# === CONFIGURE YOUR OPENAI API KEY HERE ===
openai.api_key = "Paste Open AI Key"  # 🔑 Replace with your actual OpenAI API key

# === FILE PATHS ===
TEMPLATE_PATH = "Business Prompt template.txt"
OUTPUT_TEXT_PATH = "Generated_Social_Media_Posts.txt"
OUTPUT_IMAGE_PATH = "Generated_Social_Media_Image.png"

# === PROMPT FOR BUSINESS DETAILS ===
def get_business_details():
    print("📋 Please enter the following business information:\n")

    details = {
        "business_name": input("Business Name: "),
        "business_type": input("Business Type (e.g. bakery, salon): "),
        "business_location": input("Business Location (e.g. City, State): "),
        "products_or_services": input("Products or Services (comma-separated): ").split(","),
        "target_customers": input("Target Customers (e.g. young adults, families): "),
        "brand_story": input("Brand Story: "),
        "brand_tone": input("Brand Tone (e.g. friendly, professional, fun): "),
        "promotions": input("Active Promotions (comma-separated): ").split(","),
        "testimonials": input("Customer Testimonials (comma-separated): ").split(","),
        "behind_the_scenes": input("Behind-the-Scenes Ideas (comma-separated): ").split(","),
        "events_or_news": input("Upcoming Events or News (comma-separated): ").split(","),
        "faqs": input("FAQs (comma-separated): ").split(",")
    }

    return details

# === LOAD PROMPT TEMPLATE ===
def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

# === FILL TEMPLATE WITH DATA ===
def fill_template(template, variables):
    for key, value in variables.items():
        if isinstance(value, list):
            value = ', '.join([v.strip() for v in value])
        template = template.replace(f"{{{{{key}}}}}", value)
    return template

# === GENERATE SOCIAL MEDIA CONTENT ===
def generate_content(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who writes engaging social media content for small businesses."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

# === GENERATE IMAGE PROMPT FROM CONTENT ===
def generate_image_prompt(content):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant that turns social media posts into descriptive DALL·E 3 prompts."},
            {"role": "user", "content": f"Generate a short and vivid image description for this post:\n\n{content}"}
        ],
        temperature=0.6
    )
    return response['choices'][0]['message']['content']

# === GENERATE IMAGE USING DALL·E 3 ===
def generate_image(prompt):
    print(f"\n🖼️ Generating image using DALL·E 3...")
    response = openai.Image.create(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        response_format="url",
        n=1
    )
    return response['data'][0]['url']

# === DOWNLOAD IMAGE FROM URL ===
def download_image(url, path):
    print(f"📥 Downloading image from {url} ...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Image saved to: {path}")
    else:
        print("❌ Failed to download the image.")

# === SAVE TEXT OUTPUT ===
def save_text_output(text, path):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"\n✅ Social media content saved to: {path}")

# === MAIN FUNCTION ===
def main():
    print("🚀 Social Media Content + Image Generator")
    business_data = get_business_details()

    print("\n📄 Loading template...")
    template = load_template(TEMPLATE_PATH)

    print("🧩 Filling in your business data...")
    prompt = fill_template(template, business_data)

    print("🧠 Generating social media text...")
    content = generate_content(prompt)

    print("💾 Saving text...")
    save_text_output(content, OUTPUT_TEXT_PATH)

    print("🎨 Creating image prompt...")
    image_prompt = generate_image_prompt(content)

    print(f"🧾 DALL·E Prompt:\n{image_prompt}\n")

    print("🎨 Generating image with DALL·E 3...")
    image_url = generate_image(image_prompt)

    print("💾 Downloading image...")
    download_image(image_url, OUTPUT_IMAGE_PATH)

# === RUN ===
if __name__ == "__main__":
    main()
