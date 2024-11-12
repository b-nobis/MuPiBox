import {
  CUSTOM_ELEMENTS_SCHEMA,
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  Signal,
  WritableSignal,
  computed,
  input,
  output,
  signal,
  viewChild,
} from '@angular/core'
import { IonCard, IonCardHeader, IonCardTitle, IonCol, IonGrid, IonRow } from '@ionic/angular/standalone'

import { AsyncPipe } from '@angular/common'
import { cloneDeep } from 'lodash-es'
import { Observable } from 'rxjs'
import { PlayerService } from '../player.service'

export interface SwiperData<T> {
  name: string
  imgSrc: Observable<string>
  data: T
}

@Component({
  selector: 'mupi-swiper',
  templateUrl: './swiper.component.html',
  styleUrls: ['./swiper.component.scss'],
  imports: [AsyncPipe, IonCard, IonCardHeader, IonCardTitle, IonCol, IonGrid, IonRow],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SwiperComponent<T> {
  public data = input.required<SwiperData<T>[]>()
  public roundImages = input<boolean>(false)
  public elementClicked = output<SwiperData<T>>()

  protected swiperContainer = viewChild<ElementRef>('swiper')
  protected swiper = computed(() => this.swiperContainer()?.nativeElement.swiper)
  protected pageIsShown: WritableSignal<boolean> = signal(false)

  // This is a hacky workaround for the problem that the swiper doesn't allow to scroll
  // after an ionic navigation event if the data is not updated. Thus, we copy the given
  // data here internally to fake updated data.
  // This might be removed when we have a generic API cache so we can just get new results
  // on every ionic navigation.
  protected shownData: Signal<SwiperData<T>[]>

  public constructor(private playerService: PlayerService) {
    this.shownData = computed(() => {
      if (this.pageIsShown()) {
        return cloneDeep(this.data())
      }
      return []
    })
  }

  public ionViewDidEnter(): void {
    this.pageIsShown.set(true)
  }

  public ionViewWillLeave(): void {
    this.pageIsShown.set(false)
  }

  public resetSwiperPosition(): void {
    this.swiper()?.slideTo(0, 0)
  }

  protected readText(text: string): void {
    this.playerService.sayText(text)
  }
}