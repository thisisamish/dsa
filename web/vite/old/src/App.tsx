import { useState } from "react";

const creatorSheetsMap = {
  striver: ["a2z", "sde", "75", "79"],
  lb: ["450"],
  neetcode: ["75", "150", "250"],
  leetcode: ["75", "150"],
};

// Interface for the item structure
interface Item {
  url: string;
  expanded_url: string;
  expanded_stripped_url: string;
  original_title?: string;
  step_title?: string;
  sub_step_title?: string;
  type: string;
  id_base: string;
  id: string;
  title: string;
  platform: string;
  description: string;
  // Add index signature to allow accessing properties by string key
  [key: string]: unknown;
}

interface DupesData {
  dupes_data: Item[][];
  total_items_with_dupes: number;
  total_dupes: number;
  total_items_in_sheet_before_dedupe: number;
  total_items_in_sheet_after_dedupe: number;
}

// Helper function to create an empty item structure matching the interface
const createEmptyItem = (): Item => ({
  url: "",
  expanded_url: "",
  expanded_stripped_url: "",
  original_title: "",
  step_title: "",
  sub_step_title: "",
  type: "",
  id_base: "",
  id: "",
  title: "",
  platform: "",
  description: "",
});

// Define the keys to display and their order (defined before state)
const itemKeys: (keyof Item)[] = [
  "type",
  "id",
  "id_base",
  "title",
  "expanded_stripped_url",
  "platform",
  "description",
  "original_title",
  "expanded_url",
  "url",
  "step_title",
  "sub_step_title",
];

// Helper function to create an empty selected source structure
// Keys map to the index of the duplicate item whose value was selected, or null
const createEmptySelectedSource = () => {
  const source: { [K in keyof Item]?: number | null } = {};
  itemKeys.forEach((key) => {
    source[key] = null;
  });
  return source;
};

const requiredKeys: (keyof Item)[] = [
  "expanded_stripped_url",
  "type",
  "id_base",
  "id",
  "title",
  "platform",
  "description",
];

function App() {
  const [dupesData, setDupesData] = useState<DupesData>({
    dupes_data: [],
    total_items_with_dupes: 0,
    total_dupes: 0,
    total_items_in_sheet_before_dedupe: 0,
    total_items_in_sheet_after_dedupe: 0,
  });
  const [currDupeIndex, setCurrDupeIndex] = useState<number>(0);
  const [resolvedIndices, setResolvedIndices] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  // Error state is now for localized display
  const [error, setError] = useState<string | null>(null);
  // Success state for localized display
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const [creator, setCreator] = useState<string>("striver"); // State for creator input
  const [sheetname, setSheetname] = useState<string>("sde"); // State for sheetname input

  // State for the item being built from selections/manual input
  const [newItemData, setNewItemData] = useState<Item>(createEmptyItem());
  // State to track which duplicate item index was selected for each key
  const [selectedSource, setSelectedSource] = useState<{
    [K in keyof Item]?: number | null;
  }>(createEmptySelectedSource()); // Initialize with all keys from itemKeys

  // Get the current group of duplicates to display
  const currentDupeGroup = dupesData["dupes_data"][currDupeIndex] || []; // Ensure it's always an array, even if undefined

  // Handler for fetching data
  const handleGo = () => {
    setIsLoading(true); // Start loading
    setError(null); // Clear previous errors
    setSuccessMessage(null); // Clear previous success

    fetch(
      `http://localhost:5000/api/dupes?creator=lb&sheetname=450`
    )
      .then(async (resp) => {
        setIsLoading(false); // Stop loading regardless of success/fail
        if (!resp.ok) {
          // Fetch error will set local error state
          const errorText = await resp.text(); // Attempt to read error body
          throw new Error(`HTTP error! status: ${resp.status} - ${errorText}`);
        }
        return resp.json();
      })
      .then((data: DupesData) => {
        if (
          typeof data !== "object" ||
          data === null ||
          Array.isArray(data) ||
          !Object.prototype.hasOwnProperty.call(
            data,
            "total_items_with_dupes"
          ) ||
          !Object.prototype.hasOwnProperty.call(data, "total_dupes") ||
          !Object.prototype.hasOwnProperty.call(
            data,
            "total_items_in_sheet_before_dedupe"
          ) ||
          !Object.prototype.hasOwnProperty.call(
            data,
            "total_items_in_sheet_after_dedupe"
          ) ||
          !Array.isArray(data["dupes_data"]) ||
          data["dupes_data"].some((group) => !Array.isArray(group))
        ) {
          // Data format error will set local error state
          throw new Error("Invalid data format received from API");
        }
        setResolvedIndices([]);
        setDupesData(data);
        setCurrDupeIndex(0); // Reset to the first group
        // Initialize form and selection state based on keys after data loads
        setNewItemData(createEmptyItem());
        setSelectedSource(createEmptySelectedSource());
        // Messages were cleared at the start of handleGo
      })
      .catch((error) => {
        console.error("Fetch error:", error);
        // Display fetch error locally
        setError(`Failed to fetch data: ${error.message}`);
        setDupesData({
          dupes_data: [],
          total_items_with_dupes: 0,
          total_dupes: 0,
          total_items_in_sheet_before_dedupe: 0,
          total_items_in_sheet_after_dedupe: 0,
        }); // Clear data on fetch error
        setCurrDupeIndex(0); // Reset index
        setNewItemData(createEmptyItem()); // Reset form
        setSelectedSource(createEmptySelectedSource()); // Reset selection
      });
  };

  // Handle navigation
  const handlePrev = () => {
    // Ensure save is not in progress and there's a previous group
    if (!isSaving && currDupeIndex > 0) {
      setCurrDupeIndex((prevIndex) => prevIndex - 1);
      setNewItemData(createEmptyItem()); // Reset new item data
      setSelectedSource(createEmptySelectedSource()); // Reset selection source
      setError(null); // Clear previous errors
      setSuccessMessage(null); // Clear success message
    }
  };

  const handleNext = () => {
    // Ensure save is not in progress and there's a next group
    if (!isSaving && currDupeIndex < dupesData["dupes_data"].length - 1) {
      setCurrDupeIndex((prevIndex) => prevIndex + 1);
      setNewItemData(createEmptyItem()); // Reset new item data
      setSelectedSource(createEmptySelectedSource()); // Reset selection source
      setError(null); // Clear previous errors
      setSuccessMessage(null); // Clear success message
    }
  };

  // Handler for typing into the New Item textareas
  const handleNewItemInputChange = (
    key: keyof Item,
    event: React.ChangeEvent<HTMLTextAreaElement>
  ) => {
    const { value } = event.target;
    setNewItemData((prevData) => ({
      ...prevData,
      [key]: value,
    }));
    // When the user manually types, clear the selection source for this key
    setSelectedSource((prevSource) => ({
      ...prevSource,
      [key]: null,
    }));
    // Clear validation errors when the user is changing the input
    setError(null);
    setSuccessMessage(null); // Clear success message on interaction
  };

  // Handler for clicking on a duplicate item cell
  const handleDuplicateClick = (key: keyof Item, itemIndex: number) => {
    const clickedValue = currentDupeGroup[itemIndex]?.[key]; // Use optional chaining for safety
    // Ensure clicked value is treated as string for comparison, handle undefined/null
    const clickedValueAsString = String(clickedValue ?? "");
    const newItemValueAsString = String(newItemData[key] ?? "");

    // Check if clicking the currently selected cell *and* the values match
    // The value check is important because the user might have manually changed the newItemData value
    const isCurrentlySelected =
      selectedSource[key] === itemIndex &&
      clickedValueAsString === newItemValueAsString;

    if (isCurrentlySelected) {
      // If clicking the currently selected cell, deselect it
      setNewItemData((prevData) => ({
        ...prevData,
        // Reset value to empty string or default based on createEmptyItem
        [key]: createEmptyItem()[key], // Use the default value from empty item
      }));
      setSelectedSource((prevSource) => ({
        ...prevSource,
        [key]: null,
      }));
    } else {
      // If clicking a new cell, select it *only if* the value is not empty after trimming
      // This prevents selecting empty cells if the requiredKeys validation depends on non-empty values
      const valueToSelect =
        typeof clickedValue === "string"
          ? clickedValue.trim()
          : String(clickedValue ?? "").trim();

      if (valueToSelect.length > 0 || !requiredKeys.includes(key)) {
        setNewItemData((prevData) => ({ ...prevData, [key]: clickedValue })); // Set the actual value, not the trimmed one for saving
        setSelectedSource((prevSource) => ({
          ...prevSource,
          [key]: itemIndex,
        }));
      } else {
        // Optional: Give user feedback if they clicked an empty required field cell
        setError(
          `Cannot select empty value for required field: ${String(key)}`
        );
        setSuccessMessage(null);
      }
    }
    // Clear any previous validation errors or success messages on interaction
    setError(null); // This will override the optional error set above, maybe keep it?
    // Let's keep the error set above, so only clear if successful click
    if (
      !isCurrentlySelected &&
      (String(clickedValue ?? "").trim().length > 0 ||
        !requiredKeys.includes(key))
    ) {
      setError(null);
      setSuccessMessage(null);
    }
  };

  // Handler for saving the group (posting the selected/new item)
  const handleSaveGroup = () => {
    // Check newItemData fields that are required have length > 0 after trimming
    const missingFields: string[] = [];
    requiredKeys.forEach((key) => {
      const value = newItemData[key];
      // Check if the value is a string and is empty or contains only whitespace after trimming
      if (typeof value !== "string" || value.trim().length === 0) {
        missingFields.push(String(key));
      }
    });

    if (missingFields.length > 0) {
      // Validation failed: set local error and stop
      setError(`Missing or empty required fields: ${missingFields.join(", ")}`);
      setSuccessMessage(null); // Clear success message on error
      // Don't set isSaving to true, as we are not making an API call
      return;
    }
    setIsSaving(true); // Start saving, disable button
    setError(null); // Clear previous errors before saving
    setSuccessMessage(null); // Clear previous success message before saving

    // Assume the backend endpoint expects the selected/new item data
    // The backend likely needs the original items' identifiers to know which group is being resolved.
    // For this example, we'll just send the resolved item. A real application might need
    // to send the group ID or the IDs of the original items in the group.
    // Let's assume the backend knows the group context from the save endpoint path or body.
    // The current endpoint doesn't include group ID, but let's proceed assuming it's handled implicitly or not needed.
    fetch("http://localhost:5000/api/dupes/resolve", {
      // Using a more specific resolve endpoint
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // Include creator and sheetname if the backend needs context beyond the item itself
      body: JSON.stringify({
        resolvedItem: newItemData,
        creator: "lb", // Include context
        sheetname: "450", // Include context
      }),
    })
      .then(async (response) => {
        if (!response.ok) {
          // Save error will set local error state
          const errorText = await response.text(); // Attempt to read error body
          throw new Error(
            `HTTP error! status: ${response.status} - ${errorText}`
          );
        }
        return response.json(); // Assuming the backend sends a success confirmation
      })
      .then((data) => {
        console.log("Save successful:", data);
        setResolvedIndices((prev) => [...prev, currDupeIndex]);
        // Set success message
        setSuccessMessage(`Group ${currDupeIndex + 1} saved successfully!`);
        setError(null); // Ensure error is null on success
        setCurrDupeIndex((prev) => prev + 1);
        // If the last group was just saved, reset index and data
        if (currDupeIndex >= dupesData["dupes_data"].length - 1) {
          setCurrDupeIndex(0); // Go back to the start or 0 if no more
          // If there are still groups left after filtering, index will adjust naturally.
          // If this was the last group, dupesData becomes empty, and the next render handles it.
        }
        // Reset form and selection states for the next (or current, if filtered) group
        setNewItemData(createEmptyItem());
        setSelectedSource(createEmptySelectedSource());

        // The success message will display until the next render cycle from state updates.
        // If dupesData becomes empty, the empty state message will eventually show.
      })
      .catch((error) => {
        console.error("Save failed:", error);
        // Display save error locally
        setError(`Failed to save item: ${error.message}`);
        setSuccessMessage(null); // Ensure success message is null on error
      })
      .finally(() => {
        setIsSaving(false); // End saving, re-enable button
      });
  };

  return (
    <div className="p-4 flex flex-col h-screen">
      {/* Added flex-col and h-screen for layout */}
      {/* Header and Controls */}
      <div className="flex flex-col md:flex-row justify-between items-center mb-4 gap-4">
        <h1 className="text-2xl font-bold">Duplicate Item Groups</h1>
        <div className="flex flex-col md:flex-row items-center gap-4">
          <div>
            <label htmlFor="creator" className="mr-2">
              Creator:
            </label>
            <select
              id="creator"
              className="outline rounded-sm px-1.5 py-0.5"
              value={creator} // Bind value to state
              onChange={(e) => setCreator(e.target.value)} // Update state on change
            >
              {Object.keys(creatorSheetsMap).map((creator) => (
                <option value={creator}>{creator}</option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="sheetname" className="mr-2">
              Sheetname:
            </label>
            <select
              id="sheetname"
              className="outline rounded-sm px-1.5 py-0.5"
              value={sheetname} // Bind value to state
              onChange={(e) => setSheetname(e.target.value)} // Update state on change
            >
              {creator &&
                creatorSheetsMap[creator as keyof typeof creatorSheetsMap].map(
                  (sheet) => <option value={sheet}>{sheet}</option>
                )}
            </select>
          </div>
          <button
            onClick={handleGo}
            className="px-4 py-1 rounded cursor-pointer bg-green-500 text-white hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={
              isLoading ||
              isSaving ||
              creator.trim() === "" ||
              sheetname.trim() === ""
            } // Disable while loading/saving or inputs are empty
          >
            {isLoading ? "Loading..." : "Go"}
          </button>
        </div>
        {/* Save Button - Moved here to be part of the top controls row */}
        <button
          onClick={handleSaveGroup}
          className="px-4 py-2 border rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed bg-blue-500 text-white hover:bg-blue-600"
          disabled={
            isSaving ||
            currentDupeGroup.length === 0 ||
            dupesData["dupes_data"].length === 0
          } // Disable if saving, no group, or no data
        >
          {isSaving
            ? "Saving..."
            : `Save Selected for Group ${currDupeIndex + 1}`}
        </button>
      </div>
      {/* Display errors */}
      {error && (
        <div className="p-2 mb-4 text-red-700 bg-red-100 border border-red-400 rounded">
          {error}
        </div>
      )}
      {/* Display success message */}
      {successMessage && (
        <div className="p-2 mb-4 text-green-700 bg-green-100 border border-green-400 rounded">
          {successMessage}
        </div>
      )}
      {/* Conditional Rendering based on Data */}
      {isLoading && dupesData["dupes_data"].length === 0 ? (
        <div className="p-4 text-center">Loading duplicates...</div>
      ) : dupesData["dupes_data"].length === 0 ? (
        <div className="p-4 text-center">
          No duplicate data found for the provided creator and sheetname.
        </div>
      ) : (
        <>
          {" "}
          {/* Use fragment if rendering multiple elements */}
          {/* Navigation Controls */}
          <div className="flex justify-between items-center mb-4">
            <button
              onClick={handlePrev}
              disabled={currDupeIndex === 0 || isSaving}
              className="px-4 py-2 border rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <span className="text-lg">
              Group {currDupeIndex + 1} of {dupesData["dupes_data"].length}
            </span>
            <button
              onClick={handleNext}
              disabled={
                currDupeIndex === dupesData["dupes_data"].length - 1 || isSaving
              }
              className="px-4 py-2 border rounded cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
          {/* Scrollable Container */}
          <div className="flex-grow overflow-auto border rounded-md">
            {/* Use flex-grow and overflow-auto */}
            <table className="w-full table-fixed relative">
              {resolvedIndices.includes(currDupeIndex) && (
                <div className="bg-yellow-300 opacity-65 absolute border top-0 right-0 left-0 bottom-0"></div>
              )}
              {/* table-fixed helps with column widths */}
              <thead>
                <tr>
                  {/* Fixed Header Cell for Keys (Left Sticky & Top Sticky) */}
                  <th className="sticky top-0 left-0 bg-gray-300 text-center px-4 py-2 z-30 border-b border-r min-w-[100px]">
                    Key
                  </th>
                  {/* Headers for each item in the group (Top Sticky) */}
                  {currentDupeGroup.map((_, index) => (
                    <th
                      key={`item-header-${index}`}
                      className="sticky top-0 bg-gray-300 text-left px-4 py-2 z-10 border-b border-r min-w-[250px]" // Increased min-w for duplicate columns
                    >
                      Item {index + 1}
                    </th>
                  ))}
                  {/* Fixed Header Cell for New Item (Right Sticky & Top Sticky) */}
                  <th className="sticky top-0 right-0 bg-blue-200 text-center px-4 py-2 z-30 border-b min-w-[250px]">
                    {" "}
                    {/* Increased min-w */}
                    New Item
                  </th>
                </tr>
              </thead>
              <tbody>
                {/* Rows for each key */}
                {itemKeys.map((key) => (
                  <tr key={key}>
                    {/* Sticky Data Cell for Key Name (Left Sticky) */}
                    <td className="sticky left-0 bg-gray-200 text-left px-4 py-2 z-10 border-b border-r font-semibold break-words min-w-[100px]">
                      {String(key)}
                      {requiredKeys.includes(key) ? "*" : ""}
                    </td>
                    {/* Data cells for each item's value for this key (Scrollable) */}
                    {currentDupeGroup.map((dupe, index) => {
                      const value = String(dupe[key] ?? ""); // Handle undefined/null values gracefully

                      const isSelected =
                        selectedSource[key] === index &&
                        // Also compare the actual value in newItemData in case it was manually edited then clicked again
                        value === String(newItemData[key] ?? "");

                      // Determine if this cell is clickable (only for required keys)
                      const isClickable = requiredKeys.includes(key);

                      return (
                        <td
                          key={`item-${index}-${key}`}
                          className={`border-b border-r px-4 py-2 break-words max-w-xs min-w-[250px] ${
                            isClickable
                              ? "cursor-pointer bg-blue-100 hover:bg-blue-300"
                              : "" // Add click styles only if clickable
                          } ${
                            isSelected ? "bg-yellow-200 font-bold" : "" // Highlight selected cell
                          }`}
                          onClick={
                            isClickable
                              ? () => handleDuplicateClick(key, index)
                              : undefined
                          } // Add click handler only if clickable
                        >
                          {value}
                        </td>
                      );
                    })}
                    {/* Sticky Data Cell for the New Item input (Right Sticky) */}
                    <td className="sticky right-0 border-b px-4 py-2 z-10 min-w-[250px] bg-blue-200">
                      {resolvedIndices.includes(currDupeIndex) && (
                        <div className="bg-yellow-300 opacity-65 absolute top-0 right-0 left-0 bottom-0"></div>
                      )}
                      {/* Render textarea only for required keys */}
                      {requiredKeys.includes(key) && (
                        <textarea
                          // value should always come from newItemData state
                          value={String(newItemData[key] ?? "")}
                          className={`w-full px-2 py-1 outline outline-black caret-black rounded-sm text-green-600 font-bold resize-y ${
                            // Added resize-y
                            selectedSource[key] !== null
                              ? "bg-gray-300 cursor-not-allowed" // Dim and change cursor if disabled
                              : "bg-white"
                          }`}
                          onChange={(e) => handleNewItemInputChange(key, e)}
                          // Disable input if a source is selected for this key
                          disabled={selectedSource[key] !== null}
                          rows={key === "description" ? 3 : 1} // Use more rows for description
                        />
                      )}
                      {/* Optionally display value for non-required keys if needed, otherwise cell is empty */}
                      {!requiredKeys.includes(key) &&
                        String(newItemData[key] ?? "")}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {currentDupeGroup.length === 0 && (
              <div className="p-4 text-center">
                Current group (index {currDupeIndex + 1}) is empty or invalid.
              </div>
            )}
          </div>
          {/* End Scrollable Container */}
        </>
      )}
    </div>
  );
}

export default App;
