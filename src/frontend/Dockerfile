FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y \
        nodejs \
    && rm -rf /var/lib/apt/lists/* 

RUN npm install -g yarn

WORKDIR "/sln"
COPY ["src/frontend/frontend.csproj", "src/frontend/"]
COPY ["src/frontend/app/package.json", "src/frontend/app/"]
COPY ["src/frontend/app/yarn.lock", "src/frontend/app/"]

WORKDIR "/sln/src/frontend/app"
RUN yarn > /dev/null

WORKDIR "/sln/src/frontend"
RUN dotnet restore "frontend.csproj"

WORKDIR "/sln"
COPY . .

WORKDIR "/sln/src/frontend/app"
RUN yarn build

WORKDIR "/sln/src/frontend"
RUN dotnet build "frontend.csproj" -c Release -o /sln/build

FROM build AS publish
RUN dotnet publish "frontend.csproj" -c Release -o /sln/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /sln/publish .
ENTRYPOINT ["dotnet", "frontend.dll"]