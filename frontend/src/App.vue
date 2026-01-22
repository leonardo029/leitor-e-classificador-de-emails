<template>
  <v-app>
    <AppHeader />
    
    <v-main>
      <v-container fluid class="pa-8">
        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <div class="hero-section mb-12">
              <h1 class="hero-title mb-6">
                Classificador de Emails
              </h1>
              <p class="hero-subtitle mb-4">
                Classifique emails automaticamente como <span class="highlight-productive">Produtivo</span> ou <span class="highlight-unproductive">Improdutivo</span>
              </p>
              <p class="hero-description">
                Utilize Inteligência Artificial e Processamento de Linguagem Natural para analisar seus emails e ter uma opção de resposta imediata!
              </p>
            </div>
            
            <AnalysisForm />
            <ResultList />
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import AppHeader from './components/AppHeader.vue';
import AnalysisForm from './components/AnalysisForm.vue';
import ResultList from './components/ResultList.vue';

export default defineComponent({
  name: 'App',
  components: {
    AppHeader,
    AnalysisForm,
    ResultList,
  }
});
</script>

<style scoped>
.hero-section {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  padding-top: 3rem;
}

.hero-title {
  font-size: 4rem;
  font-weight: 500;
  line-height: 1.15;
  letter-spacing: -0.02em;
  color: #000000;
  margin-bottom: 2rem;
}

.hero-subtitle {
  font-size: 1.3rem;
  font-weight: 500;
  line-height: 1.5;
  letter-spacing: -0.02em;
  color: #000000;
  margin-bottom: 1.5rem;
}

.hero-description {
  font-size: 0.9rem;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: -0.01em;
  color: #757575;
  max-width: 600px;
  margin: 0 auto;
}

.highlight-productive {
  color: rgb(0, 225, 0);
  font-weight: 500;
  letter-spacing: -0.02em;
}

.highlight-unproductive {
  color: red;
  font-weight: 500;
  letter-spacing: -0.02em;
}

@media (max-width: 960px) {
  .hero-section {
    padding-top: 2rem;
  }
  
  .hero-title {
    font-size: 2rem;
    letter-spacing: -0.02em;
    margin-bottom: 1.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.125rem;
    letter-spacing: -0.02em;
    margin-bottom: 1.25rem;
  }
  
  .hero-description {
    font-size: 0.9375rem;
    letter-spacing: -0.01em;
  }
}

@media (max-width: 600px) {
  .hero-section {
    padding-top: 1.5rem;
  }
  
  .hero-title {
    font-size: 1.75rem;
    letter-spacing: -0.02em;
    margin-bottom: 1.25rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    letter-spacing: -0.02em;
    margin-bottom: 1rem;
  }
  
  .hero-description {
    font-size: 0.875rem;
    letter-spacing: -0.01em;
  }
}
</style>
