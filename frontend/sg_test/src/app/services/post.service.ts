import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class PostService {
  private url = 'http://localhost:8000/api/';
  constructor(private httpClient: HttpClient) { }

  getPosts(){
    return this.httpClient.get(this.url, {responseType: 'json'});
  }

}
