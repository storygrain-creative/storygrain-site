STORYGRAIN CREATIVE: NETLIFY LAUNCH

1. DEPLOY
   Netlify > Add new site > Deploy manually > drag this whole folder
   (unzipped) onto the upload box. The site is live in seconds.

2. CONNECT THE DOMAIN
   Site configuration > Domain management > Add a domain > storygrain.co
   Follow Netlify's DNS steps at your registrar. HTTPS turns on automatically.

3. TURN ON FORM EMAILS
   Netlify finds the contact form on the first deploy. To get submissions
   by email, go to Site configuration > Forms > Form notifications >
   Add notification > Email notification and enter hello@storygrain.co.
   (If forms show as disabled, click "Enable form detection" and redeploy.)

4. AFTER LAUNCH
   - Test the contact form once and confirm the email arrives.
   - Paste https://storygrain.co into Facebook's Sharing Debugger
     (developers.facebook.com/tools/debug) to load the share image.
   - Add the site in Google Search Console and submit sitemap.xml.
   - Set up a Google Business Profile as a service-area business in Omaha.

THE CONTENT CHECK (storygrain.co/check)
   - It has its own form named "content-check". Your existing "any form"
     email notification already covers it. After deploying, confirm
     Forms shows both "contact" and "content-check".
   - Each submission includes every answer, the fit rating, the
     recommended needs, and a "source" field showing the ad or link.
   - For ads, link to: https://storygrain.co/check/?utm_source=facebook&utm_campaign=content-check
   - Meta Pixel: paste the pixel snippet where check/index.html says
     "Meta Pixel", then uncomment the two spots marked PIXEL.

PACKAGES PAGE (storygrain.co/packages)
   - Hidden: not linked anywhere on the site, not in the sitemap, and
     tagged so search engines skip it. Anyone with the link can view it.
   - Includes a Download PDF button for the one-sheet.

RELEASE FORM (storygrain.co/release)
   - Hidden like /packages. Talent signs with a finger or Apple Pencil.
   - Prefill the production name with a link like:
     https://storygrain.co/release/?project=Walk%20Thru%20Plans
   - Submissions land in Netlify > Forms > "release" with the signature
     as a PNG attachment. Your "any form" email notification covers it.
   - On one shared iPad, tap "Sign another release" between people.

CLIENT DELIVERY PAGES (storygrain.co/clients/<name>)
   - Hidden and password protected. The video, links and caption are
     encrypted in the page, so they can't be read without the password.
   - Walk Thru Plans: storygrain.co/clients/walk-thru-plans  (password: ask Eric or Austin)
   - Testimonials land in Netlify > Forms > "testimonial".

FILES
   index.html          the site
   check/              the Content Check quiz
   privacy/            privacy policy
   packages/           hidden pricing page + PDF
   release/            hidden talent release form
   clients/            password-protected client delivery pages
   404.html            page-not-found screen
   images/             headshots
   og-image.png        image shown when the link is shared
   favicon*, icon-*    browser and phone icons
   sitemap.xml, robots.txt, site.webmanifest, netlify.toml   setup files
