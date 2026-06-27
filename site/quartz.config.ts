import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "AI Research 技术调研",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "zh-CN",
    baseUrl: "zhao9797.github.io/ai-research",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Fraunces",
        body: "Hanken Grotesk",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#f4f5f7",
          lightgray: "#e2e4ea",
          gray: "#9499a8",
          darkgray: "#34384a",
          dark: "#14161e",
          secondary: "#3a3d9e",
          tertiary: "#6366c4",
          highlight: "rgba(58, 61, 158, 0.08)",
          textHighlight: "#c7c9ee88",
        },
        darkMode: {
          light: "#14161c",
          lightgray: "#2a2d38",
          gray: "#5c6072",
          darkgray: "#c5c8d4",
          dark: "#eceef5",
          secondary: "#8b8ee6",
          tertiary: "#a9abf0",
          highlight: "rgba(139, 142, 230, 0.12)",
          textHighlight: "#3a3d6e88",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
