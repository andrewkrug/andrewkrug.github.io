# Personal Website - Technical Influencer

A modern, responsive personal website built with 11ty (Eleventy) for technical influencers, speakers, and thought leaders.

## Features

- **Modern Design**: Clean, professional design with gradient hero sections and card-based layouts
- **Responsive**: Fully responsive design that works on all devices
- **Performance Optimized**: Fast loading with minimal JavaScript
- **SEO Ready**: Proper meta tags, Open Graph, and Twitter Card support
- **Accessibility**: Semantic HTML and proper ARIA labels

## Pages

- **Home** (`/`): Landing page featuring a hero section with introduction, overview of services, recent highlights, and call-to-action to connect
- **Biography** (`/bio/`): Detailed professional background, career highlights, and downloadable high-resolution headshot for media and event organizers
- **Where's Andrew** (`/wheres-andrew/`): Interactive event tracker showing upcoming conferences and speaking engagements, past events with video recordings, and regular locations. Includes map visualization for finding Andrew at events
- **Speaking** (`/speaking/`): Speaking topics, previous engagements, testimonials, and booking information for conference organizers
- **Writing** (`/writing/`): Collection of technical articles, blog posts, and thought leadership content with featured articles, recent publications, and links to external platforms
- **Blog** (`/blog/`): Original longer-form posts published on this site, with an RSS feed at `/feed.xml`
- **Contact** (`/contact/`): Contact information (email, Calendly booking link, social profiles) and professional service information for collaboration, speaking requests, and general inquiries. There is no contact form

## Technology Stack

- **11ty (Eleventy)**: Static site generator
- **Nunjucks**: Templating engine
- **CSS3**: Modern styling with CSS custom properties
- **Vanilla JavaScript**: Minimal JavaScript for interactions

## Getting Started

### Prerequisites

- Node.js (version 18 or higher, required by Eleventy 3.x)
- npm or yarn

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open your browser to `http://localhost:8080`

### Building for Production

```bash
npm run build
```

The built site will be in the `_site` directory.

## Customization

### Personal Information

The site is currently configured for Andrew Krug. Edit the site data in `src/_data/site.json`:

- Update name, description, and contact information
- Modify social media handles
- Customize author bio and location

### Content

- **Home Page**: Edit `src/index.njk`
- **Biography**: Edit `src/bio.njk`
- **Where's Andrew**: Edit `src/wheres-andrew.njk`
- **Speaking**: Edit `src/speaking.njk`
- **Writing**: Edit `src/writing.njk`
- **Contact**: Edit `src/contact.njk`

### Styling

The main styles are in `src/assets/css/style.css`. The design uses CSS custom properties for easy theming:

- Colors are defined in the `:root` selector
- Modify the color scheme by updating the CSS variables
- Responsive breakpoints are handled with media queries

### Images

Replace the placeholder image references in `src/images/` with professional photos:

- `hero-headshot.jpg` - Home page hero profile image
- `headshot.jpg` - Biography page image
- `headshot-high-res.jpg` - Downloadable high-resolution headshot

## Project Structure

```
├── src/
│   ├── _data/                 # Site-wide data (site.json plus YAML content files)
│   ├── _includes/
│   │   ├── nav.njk            # Navigation component
│   │   ├── footer.njk         # Footer component
│   │   └── badges.njk         # Writing/press-mention badge macros
│   ├── _layouts/
│   │   ├── base.njk           # Base HTML template
│   │   └── post.njk           # Blog post template
│   ├── assets/
│   │   └── css/
│   │       └── style.css      # Main stylesheet
│   ├── images/                # Image assets
│   ├── posts/                 # Blog post content (Markdown)
│   ├── index.njk              # Home page
│   ├── bio.njk                # Biography page
│   ├── speaking.njk           # Speaking page
│   ├── writing.njk            # Writing page
│   ├── wheres-andrew.njk      # Event/travel tracker page
│   ├── blog.njk               # Blog index page
│   ├── contact.njk            # Contact page
│   ├── 404.njk                # Not-found page
│   ├── holiday-update-2025.njk # Holiday letter page
│   ├── llms.njk               # Template for /llms.txt (AI-agent site summary)
│   ├── robots.njk             # Template for /robots.txt
│   ├── sitemap.njk            # Template for /sitemap.xml
│   └── feed.njk               # Template for /feed.xml (RSS)
├── .eleventy.js               # 11ty configuration
├── package.json               # Dependencies and scripts
└── README.md                  # This file
```

## Deployment

This site can be deployed to any static hosting service:

- **Netlify**: Connect your GitHub repository for automatic deployments
- **Vercel**: Deploy with zero configuration
- **GitHub Pages**: Use GitHub Actions for deployment
- **AWS S3**: Static website hosting
- **Cloudflare Pages**: Fast global deployment

## Development Scripts

- `npm start` or `npm run serve` - Start development server
- `npm run build` - Build for production
- `npm run debug` - Run with debug output

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Progressive enhancement for older browsers

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!