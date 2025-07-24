<template>
  <nav class="d-flex justify-content-center align-items-center gap-4 my-3">
    <router-link to="/admin" class="nav-link" :class="{ active: isActive('/admin') }">Websites</router-link>
    <router-link  to="/admin/users" class="nav-link"  :class="{ active: isActive('/admin/users') }" >Profiles</router-link>

    <router-link
      to="/admin/search"
      class="nav-link"
      :class="{ active: isActive('/admin/search') }"
    >About</router-link>

    <router-link
      to="/admin/charts"
      class="nav-link"
      :class="{ active: isActive('/admin/charts') }"
    >Subscribe</router-link>
  </nav>
</template>