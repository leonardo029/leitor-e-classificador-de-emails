<template>
  <v-file-input
    :model-value="modelValue"
    @update:model-value="$emit('update:modelValue', $event)"
    :disabled="disabled"
    :rules="rules"
    accept=".pdf,.txt"
    label="Selecione um arquivo PDF ou TXT"
    prepend-icon="mdi-file-document"
    show-size
    clearable
    variant="outlined"
    density="comfortable"
    class="input-custom"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'FileUploadTab',
  props: {
    modelValue: {
      type: Array as () => File[] | null,
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    },
    rules: {
      type: Array as () => Array<(v: File[] | null) => boolean | string>,
      default: () => []
    }
  },
  emits: ['update:modelValue']
});
</script>

<style scoped>
.input-custom {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
}

.input-custom :deep(.v-field) {
  border-radius: 6px;
  border-color: #E0E0E0;
  background-color: #FFFFFF;
  transition: border-color 0.2s ease;
}

.input-custom :deep(.v-field:hover) {
  border-color: #BDBDBD;
}

.input-custom :deep(.v-field__input) {
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #000000;
  font-size: 0.9375rem;
}

.input-custom :deep(.v-label) {
  font-weight: 400;
  letter-spacing: -0.01em;
  color: #757575;
  font-size: 0.875rem;
}

.input-custom :deep(.v-field--focused) {
  border-color: #FF7900;
}

.input-custom :deep(.v-field--focused .v-label) {
  color: #FF7900;
}
</style>
