from django.conf import settings


def global_variables(request):
    # Brand name
    brand_name = "Connectify"

    # Slogan
    slogan = "Stay connected, anytime, anywhere"

    # Version
    version = "1.0"

    # Terms and Conditions
    terms_and_conditions = """
                        <p>Please read these terms and conditions carefully before using our website.</p>
                            <p>By accessing or using our website, you agree to be bound by these terms and conditions.
                                If you do not agree with any part of these terms and conditions, you must not use our
                                website.</p>
                            <h6>1. Intellectual Property</h6>
                            <p>The content on our website, including but not limited to text, graphics, images, logos,
                                and software, is the property of our company and is protected by intellectual property
                                laws.</p>
                            <h6>2. User Conduct</h6>
                            <p>When using our website, you agree to:</p>
                            <ul>
                                <li>Comply with all applicable laws and regulations</li>
                                <li>Not engage in any unlawful or fraudulent activities</li>
                                <li>Not upload or transmit any harmful or malicious content</li>
                                <li>Not interfere with the proper functioning of our website</li>
                            </ul>
                            <h6>3. Limitation of Liability</h6>
                            <p>We shall not be liable for any direct, indirect, incidental, consequential, or punitive
                                damages arising out of your use or inability to use our website.</p>
                            <h6>4. Governing Law</h6>
                            <p>These terms and conditions shall be governed by and construed in accordance with the laws
                                of [your jurisdiction].</p>
                            <h6>5. Changes to Terms and Conditions</h6>
                            <p>We reserve the right to modify or update these terms and conditions at any time without
                                prior notice. It is your responsibility to review these terms and conditions
                                periodically.
                            </p>
                        """

    return {
        'brand_name': brand_name,
        'slogan': slogan,
        'app_version': version,
        'terms_and_conditions': terms_and_conditions,
    }
