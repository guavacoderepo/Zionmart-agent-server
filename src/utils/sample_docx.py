from langchain_core.documents import Document

documents = [
    Document(
        page_content="""
            Zion Mart is a fast-growing Nigerian e-commerce platform specializing in retail products for sports enthusiasts. 
            We offer a wide range of sporting goods, including apparel, accessories, and equipment for football, basketball, tennis, running, and fitness training. 
            Our platform is designed to make online shopping easy, secure, and fast for customers across Nigeria.

            We currently serve over 20,000 customers and process more than 3,000 orders daily. 
            Zion Mart’s mission is to inspire healthy lifestyles by providing quality sports products at affordable prices. 
            Our vision is to become Nigeria’s leading sports e-commerce brand by 2030, expanding our operations to all 36 states.
        """,
        metadata={"page": "home"}
    ),
    Document(
        page_content="""
            Zion Mart was founded in 2021 by a team of passionate sports and technology enthusiasts who saw the need for a dedicated online store for sports lovers in Nigeria. 
            We started as a small retail store in Lagos but have since expanded into a full-scale online marketplace.

            Our team includes logistics professionals, software engineers, and customer experience experts dedicated to creating a seamless shopping journey. 
            We partner with top sports brands and trusted distributors to guarantee product authenticity and quality.

            Zion Mart values customer trust, transparency, and innovation. 
            We continuously improve our systems using artificial intelligence to enhance product recommendations, optimize inventory, and deliver faster.
        """,
        metadata={"page": "about"}
    ),
    Document(
        page_content="""
            You can reach Zion Mart through the following channels:

            📍 Office Address: 24A Sports Avenue, Lekki Phase 1, Lagos, Nigeria  
            📧 Email: support@zionmart.com.ng  
            📞 Phone: +234 802 555 7284  
            🌐 Website: www.zionmart.com.ng  
            🕒 Support Hours: Monday – Saturday, 9 AM – 6 PM (WAT)

            For order-related inquiries, please include your order ID in your email.  
            For partnership or vendor registration, reach out via partnerships@zionmart.com.ng.
        """,
        metadata={"page": "contact"}
    ),
    Document(
        page_content="""
            Zion Mart’s refund and return policy ensures customer satisfaction and transparency.

            1. Returns are accepted within 30 days of purchase, provided that the product is unused, undamaged, and in its original packaging.
            2. To initiate a return, customers should contact our support team at support@zionmart.com.ng with their order ID and reason for return.
            3. Refunds are processed within 5–10 business days after the returned item passes inspection.
            4. Refunds are issued through the same payment method used for the purchase.
            5. Items such as personal protective equipment, undergarments, and nutrition products are non-returnable for hygiene reasons.

            Zion Mart reserves the right to decline returns that do not meet these conditions.
        """,
        metadata={"page": "return policy"}
    ),
    Document(
        page_content="""
            Zion Mart ensures nationwide delivery through a reliable logistics network.

            1. Orders within Lagos are typically delivered within 1–2 business days.
            2. Orders outside Lagos take between 3–5 business days, depending on location.
            3. Shipping fees vary by weight and destination; customers can view estimated costs at checkout.
            4. Once an order is confirmed, a tracking number is sent via email and SMS.
            5. Customers can track their orders in real-time on the “Track Order” page.
            6. If an order is delayed or lost, Zion Mart will issue a replacement or refund within 10 days after investigation.

            Zion Mart partners with leading courier companies such as GIG Logistics and DHL Nigeria.
        """,
        metadata={"page": "Delivery Policy"}
    ),
    Document(
        page_content="""
            Q1: How do I create an account on Zion Mart?  
            A1: Click “Sign Up” on the homepage and fill in your name, email, and password. You can also sign up using your Google account.

            Q2: What payment methods are accepted?  
            A2: We accept credit/debit cards, bank transfers, and Paystack for secure online payments.

            Q3: How do I track my order?  
            A3: After placing an order, you will receive an email and SMS containing your tracking number and a link to our order tracking page.

            Q4: Do you deliver outside Lagos?  
            A4: Yes, Zion Mart delivers nationwide through verified courier partners.

            Q5: How can I return a product?  
            A5: Contact our support team within 30 days of purchase with your order ID and reason for return. Ensure the item is unused and in original packaging.

            Q6: Does Zion Mart sell authentic products?  
            A6: Yes, all our products are sourced directly from verified manufacturers and distributors. We guarantee 100% authenticity.
        """,
        metadata={"page": "faq"}
    ),
    Document(
        page_content="""
            Zion Mart respects the privacy of all users and customers. We collect personal information solely to improve our services and enhance user experience.

            1. Information such as name, email, address, and phone number is used for order processing and delivery.
            2. Payment details are encrypted and never stored on our servers.
            3. We may use anonymized data for analytics and service improvement.
            4. Customers can request deletion of their data by contacting privacy@zionmart.com.ng.
            5. We comply with the Nigeria Data Protection Regulation (NDPR) and ensure all data is handled securely.

            By using Zion Mart, users agree to these data handling practices.
        """,
        metadata={"page": "Data Policy"}
    ),

]