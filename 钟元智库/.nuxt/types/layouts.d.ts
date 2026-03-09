import type { ComputedRef, MaybeRef } from 'vue'

type ComponentProps<T> = T extends new(...args: any) => { $props: infer P } ? NonNullable<P>
  : T extends (props: infer P, ...args: any) => any ? P
  : {}

declare module 'nuxt/app' {
  interface NuxtLayouts {
    admin: ComponentProps<typeof import("C:/Users/xinre/Desktop/15/Juxing-Space-Station/钟元智库/layouts/admin.vue").default>,
    blank: ComponentProps<typeof import("C:/Users/xinre/Desktop/15/Juxing-Space-Station/钟元智库/layouts/blank.vue").default>,
    default: ComponentProps<typeof import("C:/Users/xinre/Desktop/15/Juxing-Space-Station/钟元智库/layouts/default.vue").default>,
}
  export type LayoutKey = keyof NuxtLayouts extends never ? string : keyof NuxtLayouts
  interface PageMeta {
    layout?: MaybeRef<LayoutKey | false> | ComputedRef<LayoutKey | false>
  }
}