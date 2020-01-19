import { Component, OnInit, EventEmitter, Output } from '@angular/core';
import { Actor } from '../../models/actor';
import { ActorService } from '../../services/actor.service'
import { FlashMessagesService } from 'angular2-flash-messages';
import { HandleHttpErrorService } from '../../services/handle-http-error.service'

@Component({
  selector: 'app-actors',
  templateUrl: './actors.component.html',
  styleUrls: ['./actors.component.css']
})
export class ActorsComponent implements OnInit {
  @Output() setTitle: EventEmitter<string> = new EventEmitter();

  actors:Actor[];
  id:number;
  name:string;
  age:number;
  gender:string;
  loading:boolean = false;

  constructor(
    private actorService:ActorService,
    public flashMsg: FlashMessagesService,
    private HandleHttpError: HandleHttpErrorService
  ) { }

  ngOnInit() {
    this.setTitle.emit('Actors');
    this.getActors()
  }

  onSubmit() {
    const actor = {
      id: this.id,
      name: this.name,
      age: this.age,
      gender: this.gender
    };

    if(this.id){
      this.loading = true;
      this.actorService.editActors(actor).subscribe(resp => {
        this.loading = false;
        this.getActors()
        console.log("success: ", resp);
      }, err => {
        this.loading = false;
        this.HandleHttpError.handleError(err)
      })
      // this.actors = this.actors.filter(a => a.id !== this.id);
      // this.actors.push(actor); 
    }
    else {
      this.loading = true;
      this.actorService.addActors(actor).subscribe(resp => {
        this.loading = false;
        this.getActors()
        // this.actors.push(resp.actor); 
        console.log("success: ", resp);
      }, err => {
        this.loading = false;
        this.HandleHttpError.handleError(err)
      })
    }

    this.id = null;
    this.name = null;
    this.age = null;
    this.gender = null;
  }

  update(actor: Actor) {
    this.id = actor.id;
    this.name = actor.name;
    this.age = actor.age;
    this.gender = actor.gender;
  }

  delete(id: number) {
    this.loading = true;
    this.actorService.deleteActors(id).subscribe(resp => {
      this.loading = false;
      this.getActors()
      console.log("success: ", resp);
    }, err => {
      this.loading = false;
      this.HandleHttpError.handleError(err)
    })
    // this.actors = this.actors.filter(a => a.id !== id);
  }

  getActors() {
    this.loading = true;
    this.actorService.getActors().subscribe(actors => {
      this.loading = false;
      this.actors = actors.actors;
    }, err => {
      this.loading = false;
      this.HandleHttpError.handleError(err)
    });
  }

}
