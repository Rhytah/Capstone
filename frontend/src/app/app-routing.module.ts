import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ActorsComponent } from './pages/actors/actors.component';
import { MoviesComponent } from './pages/movies/movies.component';


const routes: Routes = [
  { path: 'actors', component: ActorsComponent },
  { path: 'movies', component: MoviesComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
