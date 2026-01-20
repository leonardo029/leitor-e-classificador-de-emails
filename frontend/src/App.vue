<template>
  <v-app>
    <AppHeader />
    
    <v-main>
      <v-container fluid class="pa-8">
        <v-row justify="center">
          <v-col cols="12" md="10" lg="8">
            <div class="text-center mb-8">
              <h1 class="text-h3 font-weight-bold mb-4 primary--text">
                Classificador Automático de Emails
              </h1>
              <p class="text-h6 text-medium-emphasis mb-2">
                Classifique emails automaticamente como <strong>Produtivo</strong> ou <strong>Improdutivo</strong>
              </p>
              <p class="text-body-1 text-medium-emphasis">
                Utilize Inteligência Artificial e Processamento de Linguagem Natural para analisar seus emails
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

<style>
#app {
  font-family: 'Roboto', sans-serif;
}
</style>
