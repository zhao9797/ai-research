import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/footer.scss"

// Custom footer override (copied over Quartz's default during the site build).
// Drops the default "Created with Quartz" credit and the upstream Quartz
// GitHub/Discord links, leaving a single link to this project's own repo.
export default (() => {
  const Footer: QuartzComponent = ({ displayClass }: QuartzComponentProps) => {
    return (
      <footer class={`${displayClass ?? ""}`}>
        <ul>
          <li>
            <a href="https://github.com/zhao9797/ai-research">GitHub</a>
          </li>
        </ul>
      </footer>
    )
  }

  Footer.css = style
  return Footer
}) satisfies QuartzComponentConstructor
