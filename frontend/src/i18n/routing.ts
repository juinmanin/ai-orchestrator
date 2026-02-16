import {defineRouting} from 'next-intl/routing';
import {createSharedPathnamesNavigation} from 'next-intl/navigation';
 
export const routing = defineRouting({
  locales: ['ko', 'en', 'ja', 'zh', 'hi', 'fr', 'es', 'ms', 'vi'],
  defaultLocale: 'en'
});
 
export const {Link, redirect, usePathname, useRouter} =
  createSharedPathnamesNavigation(routing);
