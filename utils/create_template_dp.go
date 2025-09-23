package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"
)

// Structs for JSON request/response
type GraphQLRequest struct {
	Query     string                 `json:"query"`
	Variables map[string]interface{} `json:"variables"`
}

type QuestionData struct {
	Data struct {
		Question struct {
			QuestionFrontendID string `json:"questionFrontendId"`
			Title              string `json:"title"`
		} `json:"question"`
	} `json:"data"`
}

func generateDPTemplate(slug string) error {
	url := "https://leetcode.com/graphql"
	query := `
	query getQuestionDetail($titleSlug: String!) {
		question(titleSlug: $titleSlug) {
			questionFrontendId
			title
		}
	}`

	// Prepare GraphQL request
	reqBody := GraphQLRequest{
		Query: query,
		Variables: map[string]interface{}{
			"titleSlug": slug,
		},
	}

	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return fmt.Errorf("failed to marshal GraphQL request: %v", err)
	}

	fmt.Printf("Fetching problem details for slug: %s\n", slug)

	// Make POST request
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("request failed: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != 200 {
		return fmt.Errorf("LeetCode: Request failed with status %d", resp.StatusCode)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return fmt.Errorf("failed to read response: %v", err)
	}

	var result QuestionData
	if err := json.Unmarshal(body, &result); err != nil {
		return fmt.Errorf("failed to unmarshal response: %v", err)
	}

	// Extract data
	id := result.Data.Question.QuestionFrontendID
	title := result.Data.Question.Title
	link := "https://leetcode.com/problems/" + slug
	fmt.Printf("Problem ID: %s, Title: %s, Link: %s\n", id, title, link)

	// Prepare Markdown template
	template := fmt.Sprintf(`# [%s. %s](%s)

Code available in: C++

Difficulty: 

Tags: 

Pre-requisites: 

## Approach
1. Identify the changing parameters and decide the DP dimension (1D, 2D, etc).
2. Define the recursive function: $f(i)$ or $f(i, j)$ as needed.
3. Write the base cases.
4. Write the recurrence relation.
5. Choose direction of recursion: from start or end. Choose what makes base cases simpler.
6. Optimize using memoization (top-down) or tabulation (bottom-up).
7. Try space optimization if applicable.

## Code

## C++

### Top-down/Recursive Approach
Time Complexity: $O(2^n)$

Space Complexity: $O(n)$


### Top-down/Recursive Approach (with memoization)
Time Complexity: $O(n)$

Space Complexity: $O(n)$

\`\`\`cpp

\`\`\`

### Bottom-up Approach
Time Complexity: $O(n)$

Space Complexity: $O(n)$

\`\`\`cpp

\`\`\`
`, id, title, link)

	// Format date and safe filename
	date := strings.ToLower(time.Now().Format("02-January-06"))
	baseFolder := filepath.Join("C:\\Users\\WaterShurikenNinja\\Desktop\\dsa\\daily-practice", date)

	// Remove illegal characters for Windows filenames
	safeTitle := regexp.MustCompile(`[<>:"/\\|?*]`).ReplaceAllString(title, "")
	fileName := fmt.Sprintf("%s. %s.md", id, safeTitle)
	fullPath := filepath.Join(baseFolder, fileName)

	// Create directory and write file
	if err := os.MkdirAll(baseFolder, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory: %v", err)
	}
	if err := os.WriteFile(fullPath, []byte(template), 0644); err != nil {
		return fmt.Errorf("failed to write file: %v", err)
	}

	fmt.Printf("Template created: %s\n", fullPath)
	return nil
}

func main() {
	slug := "house-robber" // Example slug; replace with user input or argument
	if err := generateDPTemplate(slug); err != nil {
		fmt.Println("Error:", err)
	}
}
