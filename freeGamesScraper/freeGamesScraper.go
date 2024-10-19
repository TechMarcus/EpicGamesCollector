package freegamesscraper

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	listscraper "main/listScraper"
	"net/http"
)

type FreeGamesPromotions struct {
	Data FreeGamesPromotionsData `json:"data"`
}
type FreeGamesPromotionsData struct {
	Catalog FreeGamesPromotionsCatalog `json:"Catalog"`
}
type FreeGamesPromotionsCatalog struct {
	SearchStore FreeGamesPromotionsSearchStore `json:"searchStore"`
}
type FreeGamesPromotionsSearchStore struct {
	Elements []FreeGamesPromotionsElements `json:"elements"`
}
type FreeGamesPromotionsElements struct {
	Title               string                      `json:"title"`
	Price               FreeGamesPromotionsPrice    `json:"price"`
	UpcommingPromotions FreeGamesUpcommingPromotion `json:"promotions"`
}
type FreeGamesUpcommingPromotion struct {
	UpcommingPromotionalOffers []FreeGamesUpcommingPromotionalOffers `json:"upcomingPromotionalOffers"`
}
type FreeGamesUpcommingPromotionalOffers struct {
	PromotionalOffers []FreeGamesPromotionalOffers `json:"promotionalOffers"`
}
type FreeGamesPromotionalOffers struct {
	StartDate string `json:"startDate"`
}
type FreeGamesPromotionsPrice struct {
	TotalPrice FreeGamesPromotionsTotalPrice `json:"totalPrice"`
}
type FreeGamesPromotionsTotalPrice struct {
	DiscountPrice int `json:"discountPrice"`
}

func CheckFreeGame() ([]string, bool, error) {
	var listurl = "https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=en-US&country=UA&allowCountries=UA"
	resp, err := http.Get(listurl)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()
	var freeGamesPromotions FreeGamesPromotions
	b, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatal(err)
	}
	err = json.Unmarshal([]byte(b), &freeGamesPromotions)
	if err != nil {
		log.Fatal(err)
	}
	elements := freeGamesPromotions.Data.Catalog.SearchStore.Elements
	if err != nil {
		return nil, false, err
	}
	var elems []string

	for _, element := range elements {
		if element.Price.TotalPrice.DiscountPrice == 0 {
			if listscraper.IsGameInList("listScraper/gameList.txt", listscraper.FormatText(element.Title)) {
				elems = append(elems, element.Title)
			}
		}
	}
	if len(elems) != 0 {
		return elems, true, nil
	}
	return nil, false, fmt.Errorf("game not found")
}

/*func UpcommingGames(element FreeGamesPromotionsElements) []string {
	var upcommingGames []string
	upcommingPromotions := element.UpcommingPromotions.UpcommingPromotionalOffers
	for _, upcommingPromotion := range upcommingPromotions {
		promotionOffers := upcommingPromotion.PromotionalOffers
		for _, promotionOffer := range promotionOffers {
			if promotionOffer.StartDate != "" {
				upcommingGames = append(upcommingGames, element.Title)
				fmt.Printf("Gamesale beggins on %s ", promotionOffer.StartDate)
				return upcommingGames

			}
		}
	}
	return nil
}
*/
