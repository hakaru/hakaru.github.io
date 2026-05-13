import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'M2DX',
  tagline: 'MIDI 2.0 + DX7-compatible FM synthesizer for iOS',
  favicon: 'img/favicon.ico',
  url: 'https://hakaru.net',
  baseUrl: '/M2DX-docs/',
  trailingSlash: true,
  organizationName: 'hakaru',
  projectName: 'hakaru.github.io',
  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'de', 'es', 'fr', 'it', 'ja', 'ko', 'nl', 'pt-BR', 'sv', 'zh-Hant'],
  },
  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: undefined,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
        gtag: {
          trackingID: 'G-N0830V28FD',
          anonymizeIP: false,
        },
      } satisfies Preset.Options,
    ],
  ],
  themeConfig: {
    image: 'img/m2dx-icon.png',
    navbar: {
      title: 'M2DX',
      logo: {
        alt: 'M2DX',
        src: 'img/m2dx-icon.png',
      },
      items: [
        {
          href: '/M2DX-support/',
          label: 'Main site',
          position: 'right',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
      ],
    },
    colorMode: {
      defaultMode: 'dark',
      respectPrefersColorScheme: true,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
