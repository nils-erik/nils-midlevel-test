import { Component, OnInit } from '@angular/core';
import { PostService } from './services/post.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent implements OnInit {
  itemsOk:any;
  issuesWarningCount:any;
  issuesCriticalCount:any;
  titles:any;
  inspector_names:any;
  warnings:any;
  criticals:any;
  rows:any;
  constructor(private service:PostService) {}

  ngOnInit() {
    this.itemsOk = [];
    this.issuesWarningCount = [];
    this.issuesCriticalCount = [];
    this.titles = [];
    this.inspector_names = [];
    this.warnings = [];
    this.criticals = [];
    this.rows = [];
      this.service.getPosts()
        .subscribe(response => {
          let k: keyof typeof response;
          for (k in response) {

            let v = response[k];
            let text = JSON.parse(JSON.stringify(v));
            for (let key in text) {
              if (key == "itemsOk") {
                this.itemsOk.push(text.itemsOk);
              } else if (key == "issuesWarningCount") {
                this.issuesWarningCount.push(text.issuesWarningCount);
              } else if (key == "issuesCriticalCount") {
                this.issuesCriticalCount.push(text.issuesCriticalCount);
              } else if (key == "title") {
                this.titles.push(text.title);
              } else if (key == "inspectorName") {
                this.inspector_names.push(text.inspectorName);
              } else if (key == "Warning") {
                this.warnings.push(text.Warning);
              } else if (key == "Critical") {
                this.criticals.push(text.Critical);
                this.rows.push([this.titles[this.titles.length-1], this.inspector_names[this.inspector_names.length-1], this.warnings[this.warnings.length-1], this.criticals[this.criticals.length-1]])
              }
            }
          }
        });
  }

  ngstyle_row(warning:any, critical:any) {
    if (warning > 0) {
      return 'yellow'
    } else if (critical > 0) {
      return 'red'
    } else {
      return 'white'
    }
  }

}

