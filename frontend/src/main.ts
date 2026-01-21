import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

import 'vuetify/styles';
import './styles/global.css';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { aliases, mdi } from 'vuetify/iconsets/mdi';

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#FF7900',
          secondary: '#757575',
          accent: '#FF7900',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
          background: '#FFFFFF',
          surface: '#FFFFFF',
          'on-surface': '#000000',
          'on-background': '#000000',
        },
      },
    },
  },
  defaults: {
    global: {
      ripple: false,
    },
  },
});

const pinia = createPinia();

createApp(App)
  .use(pinia)
  .use(vuetify)
  .mount('#app');
